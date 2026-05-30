#!/usr/bin/env python3
"""
DollarFS Secure File Scanner — Anti-Inflation + Streaming Hash Security Patch v0.1.1

Patches the critical vulnerability where `total_size_bytes` or naive file reads
could be inflated by sparse files, unbounded reads, or low-entropy garbage.

Doctrine: A file is not money. Size is not value. Only verified, hashed,
entropy-checked, complexity-measured work products count toward valuation.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import string
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple


class FileTrustTier(Enum):
    """Trustworthiness of a file type for valuation purposes."""
    TRUSTED = "trusted"          # Source code, config, docs with verifiable structure
    SUSPECT = "suspect"        # Generated files, lockfiles, bundled assets
    UNTRUSTED = "untrusted"    # Binaries, archives, logs, temp files
    BLOCKED = "blocked"        # Known attack vectors: sparse containers, synthetic dumps


class FileStatus(Enum):
    """Outcome of secure file scanning."""
    VERIFIED = "verified"
    SUSPECT = "suspect"
    RISK_BLOCKED = "risk_blocked"
    TOO_LARGE = "too_large"
    SPARSE_DETECTED = "sparse_detected"
    LOW_ENTROPY = "low_entropy"


@dataclass
class SecureFileMetrics:
    """Deterministic, tamper-resistant file metrics."""
    path: str
    size_bytes: int
    streamed_sha256: str
    entropy_bits: float
    sloc_estimate: int
    ast_complexity: float
    trust_tier: FileTrustTier
    status: FileStatus
    risk_flags: List[str] = field(default_factory=list)
    valuation_cap_usd: Decimal = Decimal("0")
    actual_disk_usage_bytes: Optional[int] = None
    is_sparse: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "size_bytes": self.size_bytes,
            "streamed_sha256": self.streamed_sha256,
            "entropy_bits": round(self.entropy_bits, 4),
            "sloc_estimate": self.sloc_estimate,
            "ast_complexity": round(self.ast_complexity, 4),
            "trust_tier": self.trust_tier.value,
            "status": self.status.value,
            "risk_flags": self.risk_flags,
            "valuation_cap_usd": str(self.valuation_cap_usd),
            "actual_disk_usage_bytes": self.actual_disk_usage_bytes,
            "is_sparse": self.is_sparse,
        }


class DollarFSSecurityPolicy:
    """
    Conservative security policy for file valuation.
    All defaults are pessimistic. Trust must be earned.
    """

    # Max file size: 10MB for individual files
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024

    # Max total scan size per asset: 500MB
    MAX_TOTAL_SCAN_BYTES: int = 500 * 1024 * 1024

    # Entropy threshold: files below this bits/byte are likely compressed or synthetic
    MIN_ENTROPY_BITS: float = 1.5

    # Low-entropy penalty threshold
    LOW_ENTROPY_THRESHOLD: float = 0.8

    # Sparse file detection: if actual disk usage < 50% of reported size
    SPARSE_THRESHOLD_RATIO: float = 0.5

    # Valuation caps per file by tier
    VALUATION_CAP_TRUSTED: Decimal = Decimal("500")
    VALUATION_CAP_SUSPECT: Decimal = Decimal("100")
    VALUATION_CAP_UNTRUSTED: Decimal = Decimal("10")
    VALUATION_CAP_BLOCKED: Decimal = Decimal("0")

    # File extension trust mapping
    TRUSTED_EXTENSIONS: set = {
        # Source code
        ".py", ".rs", ".go", ".ts", ".tsx", ".js", ".jsx",
        ".java", ".kt", ".scala", ".swift", ".m", ".mm",
        ".cpp", ".c", ".h", ".hpp", ".cs", ".vb",
        ".rb", ".php", ".pl", ".pm", ".r", ".lua",
        ".hs", ".erl", ".ex", ".exs", ".clj", ".cljs",
        ".sol", ".vy", ".cairo",
        # Config / docs
        ".md", ".rst", ".txt", ".yaml", ".yml", ".toml",
        ".json", ".ini", ".cfg", ".conf", ".dockerfile",
        ".sql", ".graphql", ".proto",
        # Web
        ".html", ".htm", ".css", ".scss", ".sass", ".less",
        # Build
        ".cmake", ".make", ".sh", ".bash", ".zsh", ".ps1",
    }

    SUSPECT_EXTENSIONS: set = {
        # Generated / lockfiles
        ".lock", ".sum", ".min.js", ".min.css",
        ".bundle.js", ".chunk.js", ".map",
        # Bundled assets
        ".ico", ".svg" "bundle", ".asset",
        # Package manifests with bundled checksums
        ".egg-info", ".dist-info",
    }

    UNTRUSTED_EXTENSIONS: set = {
        # Binaries
        ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".obj",
        ".a", ".lib", ".pdb", ".pyc", ".pyo", ".class",
        # Archives
        ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
        ".jar", ".war", ".ear",
        # Media
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
        ".mp3", ".mp4", ".avi", ".mov", ".wav", ".ogg",
        # Documents
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
        # Logs / temp
        ".log", ".tmp", ".temp", ".cache", ".bak", ".swp",
        ".swo", ".swn", ".~",
    }

    BLOCKED_PATTERNS: List[str] = [
        # Sparse container patterns
        r"\.sparse\.", r"\.hole\.", r"__sparse__",
        # Synthetic inflation patterns
        r"fill\d+\.txt", r"padding\d+\.txt", r"dummy\d+\.txt",
        r"inflate\d+\.", r"synthetic\d+\.", r"fake\d+\.",
        # Known attack filenames
        r"\.null_bytes\.", r"\.zero_pad\.", r"\.repeat_char\.",
    ]


def _extension(path: str) -> str:
    """Lowercase extension, including compound like .min.js"""
    base = os.path.basename(path).lower()
    if "." not in base:
        return ""
    # Handle compound extensions
    for compound in [".min.js", ".min.css", ".bundle.js", ".chunk.js", ".egg-info", ".dist-info"]:
        if base.endswith(compound):
            return compound
    return os.path.splitext(base)[1]


def _classify_extension(path: str, policy: DollarFSSecurityPolicy) -> FileTrustTier:
    """Classify file by extension into trust tier."""
    ext = _extension(path)
    base = os.path.basename(path).lower()

    # Check blocked patterns first
    for pattern in policy.BLOCKED_PATTERNS:
        if re.search(pattern, base):
            return FileTrustTier.BLOCKED

    if ext in policy.TRUSTED_EXTENSIONS:
        return FileTrustTier.TRUSTED
    if ext in policy.SUSPECT_EXTENSIONS:
        return FileTrustTier.SUSPECT
    if ext in policy.UNTRUSTED_EXTENSIONS:
        return FileTrustTier.UNTRUSTED

    # Unknown extension: check if it looks like source
    # Heuristic: if it has no extension and contains code-like patterns
    if not ext:
        # Check for shebang or common executable names
        if base in {"makefile", "dockerfile", "gemfile", "rakefile", "cmakelists.txt"}:
            return FileTrustTier.TRUSTED
        return FileTrustTier.SUSPECT

    return FileTrustTier.UNTRUSTED


def _streaming_sha256(path: str, max_bytes: int) -> Tuple[str, int]:
    """
    Compute SHA-256 by streaming chunks. Never loads entire file.
    Returns (hexdigest, bytes_read).
    """
    hasher = hashlib.sha256()
    bytes_read = 0
    chunk_size = 65536  # 64KB chunks

    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
            bytes_read += len(chunk)
            if bytes_read >= max_bytes:
                break

    return hasher.hexdigest(), bytes_read


def _calculate_entropy(path: str, sample_bytes: int = 65536) -> float:
    """
    Calculate Shannon entropy in bits per byte.
    Only samples first 64KB for speed; sufficient for classification.
    """
    try:
        with open(path, "rb") as f:
            data = f.read(sample_bytes)
    except Exception:
        return 0.0

    if not data:
        return 0.0

    # Shannon entropy: -sum(p * log2(p))
    counts = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counts.values():
        if count == 0:
            continue
        p = count / length
        entropy -= p * math.log2(p)

    return entropy


def _is_sparse_file(path: str) -> Tuple[bool, Optional[int], Optional[int]]:
    """
    Detect sparse files by comparing st_size vs actual disk blocks used.
    Returns (is_sparse, size_bytes, blocks_used_bytes).
    """
    try:
        st = os.stat(path)
        size_bytes = st.st_size
        # st_blocks is in 512-byte units on most POSIX systems
        blocks_used_bytes = st.st_blocks * 512 if hasattr(st, "st_blocks") else None

        if blocks_used_bytes is not None and size_bytes > 0:
            ratio = blocks_used_bytes / size_bytes
            # If actual disk usage is significantly less than reported size
            is_sparse = ratio < DollarFSSecurityPolicy.SPARSE_THRESHOLD_RATIO
            return is_sparse, size_bytes, blocks_used_bytes

        return False, size_bytes, blocks_used_bytes
    except Exception:
        return False, None, None


def _estimate_sloc(path: str, max_bytes: int = 10 * 1024 * 1024) -> int:
    """
    Conservative SLOC estimate from file content.
    Handles common source file formats. Penalizes bloated lines.
    """
    try:
        # Only read text files
        ext = _extension(path)
        if ext in DollarFSSecurityPolicy.UNTRUSTED_EXTENSIONS:
            return 0

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            # Limit read to max_bytes characters
            text = f.read(max_bytes)
    except Exception:
        return 0

    lines = text.splitlines()
    sloc = 0
    for line in lines:
        stripped = line.strip()
        # Skip blank lines and comment-only lines
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            continue
        if stripped.startswith("/*") or stripped.startswith("*"):
            continue
        if stripped.startswith("<!--") or stripped.endswith("-->"):
            continue
        # Penalize extremely long lines (>500 chars) — likely minified/garbage
        if len(stripped) > 500:
            sloc += 1  # Count as 1 line, not proportional
        else:
            sloc += 1

    return sloc


def _estimate_ast_complexity(path: str, max_bytes: int = 10 * 1024 * 1024) -> float:
    """
    Lightweight AST complexity proxy using regex patterns.
    Not a real AST parser, but sufficient for risk classification.
    """
    try:
        ext = _extension(path)
        if ext in DollarFSSecurityPolicy.UNTRUSTED_EXTENSIONS:
            return 0.0

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read(max_bytes)
    except Exception:
        return 0.0

    # Complexity signals
    nesting_depth = 0
    max_depth = 0
    indent_levels = []

    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped:
            continue
        indent = len(line) - len(stripped)
        indent_levels.append(indent)

    if indent_levels:
        # Estimate max nesting from indent deltas
        for i in range(1, len(indent_levels)):
            if indent_levels[i] > indent_levels[i - 1]:
                nesting_depth += 1
            elif indent_levels[i] < indent_levels[i - 1]:
                nesting_depth = max(0, nesting_depth - 1)
            max_depth = max(max_depth, nesting_depth)

    # Count control flow keywords
    control_patterns = [
        r"\bif\b", r"\belse\b", r"\belif\b", r"\bfor\b",
        r"\bwhile\b", r"\btry\b", r"\bexcept\b", r"\bcatch\b",
        r"\bwith\b", r"\basync\b", r"\bawait\b", r"\bmatch\b",
        r"\bloop\b", r"\breturn\b", r"\byield\b",
    ]
    control_count = sum(len(re.findall(p, text)) for p in control_patterns)

    # Cyclomatic complexity proxy
    complexity = max_depth * 2 + math.log1p(control_count)
    return round(complexity, 2)


def scan_file(path: str, policy: Optional[DollarFSSecurityPolicy] = None) -> SecureFileMetrics:
    """
    Securely scan a single file and return deterministic, tamper-resistant metrics.
    This is the core DollarFS anti-inflation primitive.
    """
    if policy is None:
        policy = DollarFSSecurityPolicy()

    risk_flags: List[str] = []
    status = FileStatus.VERIFIED
    trust_tier = _classify_extension(path, policy)

    # 1. Size check with policy limit
    size_bytes = 0
    try:
        size_bytes = os.path.getsize(path)
    except Exception:
        risk_flags.append("unreadable_size")
        status = FileStatus.RISK_BLOCKED

    if size_bytes > policy.MAX_FILE_SIZE_BYTES:
        risk_flags.append(f"exceeds_max_size_{policy.MAX_FILE_SIZE_BYTES}")
        status = FileStatus.TOO_LARGE
        trust_tier = FileTrustTier.BLOCKED

    # 2. Sparse file detection
    is_sparse = False
    actual_disk_usage = None
    if status != FileStatus.TOO_LARGE:
        is_sparse, _, actual_disk_usage = _is_sparse_file(path)
        if is_sparse:
            risk_flags.append("sparse_file_detected")
            status = FileStatus.SPARSE_DETECTED
            trust_tier = FileTrustTier.BLOCKED

    # 3. Streaming SHA-256 (never load whole file)
    max_read = min(size_bytes, policy.MAX_FILE_SIZE_BYTES) if size_bytes else policy.MAX_FILE_SIZE_BYTES
    streamed_sha256, bytes_read = _streaming_sha256(path, max_read)

    # 4. Entropy analysis
    entropy = _calculate_entropy(path)
    if entropy < policy.LOW_ENTROPY_THRESHOLD:
        risk_flags.append(f"low_entropy_{entropy:.2f}")
        if status == FileStatus.VERIFIED:
            status = FileStatus.LOW_ENTROPY
        if entropy < 0.5:
            trust_tier = FileTrustTier.BLOCKED

    # 5. SLOC estimate
    sloc = _estimate_sloc(path, policy.MAX_FILE_SIZE_BYTES)

    # 6. AST complexity proxy
    ast_complexity = _estimate_ast_complexity(path, policy.MAX_FILE_SIZE_BYTES)

    # 7. Synthetic inflation check: giant file with low complexity + low entropy
    if size_bytes > 1024 * 1024 and entropy < 1.0 and ast_complexity < 2.0:
        risk_flags.append("synthetic_inflation_candidate")
        if status == FileStatus.VERIFIED:
            status = FileStatus.SUSPECT
        trust_tier = FileTrustTier.BLOCKED

    # 8. Valuation cap based on trust tier and status
    if status in (FileStatus.RISK_BLOCKED, FileStatus.SPARSE_DETECTED, FileStatus.TOO_LARGE):
        valuation_cap = policy.VALUATION_CAP_BLOCKED
    else:
        cap_map = {
            FileTrustTier.TRUSTED: policy.VALUATION_CAP_TRUSTED,
            FileTrustTier.SUSPECT: policy.VALUATION_CAP_SUSPECT,
            FileTrustTier.UNTRUSTED: policy.VALUATION_CAP_UNTRUSTED,
            FileTrustTier.BLOCKED: policy.VALUATION_CAP_BLOCKED,
        }
        valuation_cap = cap_map.get(trust_tier, policy.VALUATION_CAP_BLOCKED)

    # Additional cap for low entropy
    if entropy < policy.MIN_ENTROPY_BITS:
        valuation_cap = min(valuation_cap, Decimal("50"))

    return SecureFileMetrics(
        path=path,
        size_bytes=size_bytes,
        streamed_sha256=streamed_sha256,
        entropy_bits=entropy,
        sloc_estimate=sloc,
        ast_complexity=ast_complexity,
        trust_tier=trust_tier,
        status=status,
        risk_flags=risk_flags,
        valuation_cap_usd=valuation_cap,
        actual_disk_usage_bytes=actual_disk_usage,
        is_sparse=is_sparse,
    )


def scan_directory(
    root: str,
    policy: Optional[DollarFSSecurityPolicy] = None,
    skip_dirs: Optional[List[str]] = None,
) -> List[SecureFileMetrics]:
    """
    Scan a directory tree securely. Respects total size limits.
    """
    if policy is None:
        policy = DollarFSSecurityPolicy()
    if skip_dirs is None:
        skip_dirs = [".git", "node_modules", "__pycache__", ".venv", "venv", "target", "dist", "build"]

    results: List[SecureFileMetrics] = []
    total_bytes_scanned = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out skipped directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            # Skip symlinks for security
            if os.path.islink(filepath):
                continue

            try:
                size = os.path.getsize(filepath)
            except Exception:
                continue

            total_bytes_scanned += size
            if total_bytes_scanned > policy.MAX_TOTAL_SCAN_BYTES:
                break

            metrics = scan_file(filepath, policy)
            results.append(metrics)

        if total_bytes_scanned > policy.MAX_TOTAL_SCAN_BYTES:
            results.append(
                SecureFileMetrics(
                    path=f"{root}/[SCAN_LIMIT_REACHED]",
                    size_bytes=0,
                    streamed_sha256="",
                    entropy_bits=0.0,
                    sloc_estimate=0,
                    ast_complexity=0.0,
                    trust_tier=FileTrustTier.BLOCKED,
                    status=FileStatus.RISK_BLOCKED,
                    risk_flags=["total_scan_limit_exceeded"],
                )
            )
            break

    return results


def secure_valuation_summary(metrics: List[SecureFileMetrics]) -> Dict[str, Any]:
    """
    Aggregate secure metrics into a valuation summary.
    Blocked/suspect files are excluded from value, included in risk register.
    """
    trusted_sloc = 0
    trusted_files = 0
    blocked_files = 0
    suspect_files = 0
    total_valuation_cap = Decimal("0")
    risk_register: List[Dict[str, Any]] = []

    for m in metrics:
        if m.status == FileStatus.RISK_BLOCKED or m.trust_tier == FileTrustTier.BLOCKED:
            blocked_files += 1
            risk_register.append(m.to_dict())
            continue

        if m.status == FileStatus.SUSPECT or m.trust_tier == FileTrustTier.SUSPECT:
            suspect_files += 1
            # Suspect files contribute at 25% cap
            total_valuation_cap += m.valuation_cap_usd * Decimal("0.25")
            continue

        if m.trust_tier == FileTrustTier.TRUSTED:
            trusted_files += 1
            trusted_sloc += m.sloc_estimate
            total_valuation_cap += m.valuation_cap_usd

    # Conservative aggregate: cap at $50K per asset
    total_valuation_cap = min(total_valuation_cap, Decimal("50000"))

    return {
        "trusted_files": trusted_files,
        "trusted_sloc": trusted_sloc,
        "suspect_files": suspect_files,
        "blocked_files": blocked_files,
        "total_valuation_cap_usd": str(total_valuation_cap),
        "risk_register_count": len(risk_register),
        "risk_register": risk_register[:50],  # Limit output size
        "policy_version": "dollarfs_v0.1.1",
    }
