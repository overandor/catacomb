#!/usr/bin/env python3
"""
Regression tests for DollarFS Secure File Scanner v0.1.1

Proves that synthetic inflation attacks cannot create fake value.
"""

import os
import sys
import tempfile
import math
from decimal import Decimal

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dollarfs_secure import (
    scan_file,
    scan_directory,
    secure_valuation_summary,
    DollarFSSecurityPolicy,
    FileStatus,
    FileTrustTier,
)


def test_sparse_file_cannot_create_fake_value():
    """
    A 100MB sparse file must be detected and blocked from valuation.
    On macOS/APFS, st_blocks may not reflect sparseness, so we also
    verify by checking that a huge file with tiny real content gets
    flagged via synthetic-inflation heuristics.
    """
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
        path = f.name
        # Seek to create a sparse-like file (100MB with only 1 byte actual data)
        f.seek(100 * 1024 * 1024)  # 100MB
        f.write(b"X")

    try:
        metrics = scan_file(path)
        # On macOS/APFS, is_sparse may be False because st_blocks is unreliable,
        # but the file MUST still be blocked by synthetic-inflation heuristics
        assert (
            metrics.is_sparse
            or metrics.status == FileStatus.SPARSE_DETECTED
            or "synthetic_inflation_candidate" in metrics.risk_flags
            or metrics.trust_tier == FileTrustTier.BLOCKED
        ), f"Expected blocked for sparse/inflation, got {metrics.to_dict()}"
        assert metrics.valuation_cap_usd == Decimal("0"), "Sparse/synthetic files must have zero valuation cap"
    finally:
        os.unlink(path)


def test_low_entropy_giant_file_blocked():
    """
    A 2MB file of repeated 'A' characters must be flagged as synthetic inflation.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        path = f.name
        f.write("A" * (2 * 1024 * 1024))

    try:
        metrics = scan_file(path)
        assert metrics.entropy_bits < 0.5, f"Expected very low entropy, got {metrics.entropy_bits}"
        assert "low_entropy" in str(metrics.risk_flags)
        assert metrics.trust_tier == FileTrustTier.BLOCKED, f"Expected BLOCKED, got {metrics.trust_tier}"
        assert metrics.valuation_cap_usd == Decimal("0")
    finally:
        os.unlink(path)


def test_trusted_source_file_valued():
    """
    A real Python file with actual complexity should be trusted and valued.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        path = f.name
        f.write("""
def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result
    
    def subtract(self, a, b):
        return a - b
""")

    try:
        metrics = scan_file(path)
        assert metrics.trust_tier == FileTrustTier.TRUSTED
        assert metrics.status == FileStatus.VERIFIED
        assert metrics.sloc_estimate > 5
        assert metrics.ast_complexity > 0
        assert metrics.valuation_cap_usd > Decimal("0")
        assert len(metrics.streamed_sha256) == 64
    finally:
        os.unlink(path)


def test_untrusted_binary_zero_value():
    """
    A .exe file must be untrusted and capped near zero.
    """
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".exe", delete=False) as f:
        path = f.name
        f.write(b"\x00\x01\x02\x03" * 1024)

    try:
        metrics = scan_file(path)
        assert metrics.trust_tier == FileTrustTier.UNTRUSTED
        assert metrics.valuation_cap_usd == Decimal("10")
    finally:
        os.unlink(path)


def test_blocked_pattern_filename():
    """
    Files matching blocked patterns must be blocked regardless of content.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix="inflate1.txt", delete=False) as f:
        path = f.name
        f.write(" legitimate looking content ")

    try:
        metrics = scan_file(path)
        assert metrics.trust_tier == FileTrustTier.BLOCKED, f"Expected BLOCKED, got {metrics.trust_tier}"
        assert metrics.valuation_cap_usd == Decimal("0")
    finally:
        os.unlink(path)


def test_streaming_hash_deterministic():
    """
    Same file must always produce same SHA-256.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        path = f.name
        f.write("# deterministic content\nprint('hello')\n")

    try:
        m1 = scan_file(path)
        m2 = scan_file(path)
        assert m1.streamed_sha256 == m2.streamed_sha256
        assert len(m1.streamed_sha256) == 64
    finally:
        os.unlink(path)


def test_scan_directory_respects_limits():
    """
    Directory scan must respect skip_dirs and total size limits.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a real file
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("print('hello')\n")

        # Create a file in skipped dir
        os.makedirs(os.path.join(tmpdir, "node_modules", "test"))
        with open(os.path.join(tmpdir, "node_modules", "test", "pkg.js"), "w") as f:
            f.write("module.exports = {}\n")

        results = scan_directory(tmpdir)
        paths = [r.path for r in results]
        assert any("main.py" in p for p in paths)
        assert not any("node_modules" in p for p in paths)


def test_secure_valuation_summary_excludes_blocked():
    """
    Blocked files must not contribute to valuation summary.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Trusted file
        with open(os.path.join(tmpdir, "real.py"), "w") as f:
            f.write("def real(): pass\n")

        # Blocked file (sparse)
        sparse_path = os.path.join(tmpdir, "sparse.bin")
        with open(sparse_path, "wb") as f:
            f.seek(1024 * 1024 * 100)  # 100MB sparse
            f.write(b"X")

        results = scan_directory(tmpdir)
        summary = secure_valuation_summary(results)

        assert summary["blocked_files"] >= 1
        assert summary["trusted_files"] >= 1
        # Total cap should be bounded
        cap = Decimal(summary["total_valuation_cap_usd"])
        assert cap <= Decimal("50000")


def test_max_file_size_policy():
    """
    Files exceeding MAX_FILE_SIZE_BYTES must be capped.
    """
    policy = DollarFSSecurityPolicy()
    policy.MAX_FILE_SIZE_BYTES = 1024  # 1KB for testing

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        path = f.name
        f.write("x = 1\n" * 500)  # ~2KB

    try:
        metrics = scan_file(path, policy)
        assert metrics.status == FileStatus.TOO_LARGE
        assert metrics.valuation_cap_usd == Decimal("0")
    finally:
        os.unlink(path)


def test_entropy_calculation_reasonable():
    """
    Entropy should distinguish structured text from garbage.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        path = f.name
        f.write("import os\nimport sys\n\ndef main():\n    print('hello')\n")

    try:
        metrics = scan_file(path)
        # Python source has moderate-high entropy (~4-5 bits/byte)
        assert metrics.entropy_bits > 2.0, f"Expected entropy > 2.0, got {metrics.entropy_bits}"
    finally:
        os.unlink(path)


def run_all_tests():
    """Run all regression tests."""
    tests = [
        test_sparse_file_cannot_create_fake_value,
        test_low_entropy_giant_file_blocked,
        test_trusted_source_file_valued,
        test_untrusted_binary_zero_value,
        test_blocked_pattern_filename,
        test_streaming_hash_deterministic,
        test_scan_directory_respects_limits,
        test_secure_valuation_summary_excludes_blocked,
        test_max_file_size_policy,
        test_entropy_calculation_reasonable,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {test.__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
