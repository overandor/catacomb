#!/usr/bin/env python3
"""Catacomb - Deterministic Agent Stack for Repo Revival."""
import os
import sys
import click
from rich.console import Console
from rich.table import Table
from orchestrator import CatacombOrchestrator

console = Console()


@click.group()
def cli():
    """Catacomb: Find repos you can revive with deterministic scoring."""
    pass


@cli.command()
@click.argument('topic')
@click.option('--limit', '-l', default=10, help='Number of repos to analyze')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.option('--token', '-t', help='GitHub API token (or set GITHUB_TOKEN env var)')
def topic(topic, limit, verbose, token):
    """Find high-value interventions by GitHub topic."""
    console.print(f"[bold blue]Searching for interventions with topic: {topic}[/bold blue]\n")
    
    github_token = token or os.getenv("GITHUB_TOKEN")
    orchestrator = CatacombOrchestrator(github_token)
    
    with console.status("[bold green]Analyzing repositories..."):
        results = orchestrator.analyze_topic(topic, limit)
    
    if not results:
        console.print("[yellow]No repositories found.[/yellow]")
        return
    
    # Display results
    console.print(orchestrator.format_output(results, verbose=verbose))
    
    # Summary table
    table = Table(title=f"Top {len(results)} Interventions")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Repo", style="magenta")
    table.add_column("Intervention", style="green", width=20)
    table.add_column("Score", style="green", width=8)
    table.add_column("Effort", style="yellow", width=8)
    table.add_column("Stars", style="yellow", width=8)
    
    for i, result in enumerate(results[:10], 1):
        if "error" not in result:
            analysis = result.get("analysis", {})
            best_intervention = analysis.get("best_intervention", {})
            table.add_row(
                str(i),
                result["repo"],
                best_intervention.get("name", "N/A")[:20],
                f"{analysis.get('intervention_score', 0):.1f}",
                f"{best_intervention.get('effort_days', 0)}d",
                str(result["repo_data"].get("stars", 0))
            )
    
    console.print("\n")
    console.print(table)


@cli.command()
@click.argument('username')
@click.option('--limit', '-l', default=10, help='Number of repos to analyze')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.option('--token', '-t', help='GitHub API token (or set GITHUB_TOKEN env var)')
def user(username, limit, verbose, token):
    """Find high-value interventions by GitHub username."""
    console.print(f"[bold blue]Searching interventions for user: {username}[/bold blue]\n")
    
    github_token = token or os.getenv("GITHUB_TOKEN")
    orchestrator = CatacombOrchestrator(github_token)
    
    with console.status("[bold green]Analyzing repositories..."):
        results = orchestrator.analyze_user(username, limit)
    
    if not results:
        console.print("[yellow]No repositories found.[/yellow]")
        return
    
    # Display results
    console.print(orchestrator.format_output(results, verbose=verbose))
    
    # Summary table
    table = Table(title=f"Top {len(results)} Interventions")
    table.add_column("Rank", style="cyan", width=6)
    table.add_column("Repo", style="magenta")
    table.add_column("Intervention", style="green", width=20)
    table.add_column("Score", style="green", width=8)
    table.add_column("Effort", style="yellow", width=8)
    table.add_column("Stars", style="yellow", width=8)
    
    for i, result in enumerate(results[:10], 1):
        if "error" not in result:
            analysis = result.get("analysis", {})
            best_intervention = analysis.get("best_intervention", {})
            table.add_row(
                str(i),
                result["repo"],
                best_intervention.get("name", "N/A")[:20],
                f"{analysis.get('intervention_score', 0):.1f}",
                f"{best_intervention.get('effort_days', 0)}d",
                str(result["repo_data"].get("stars", 0))
            )
    
    console.print("\n")
    console.print(table)


@cli.command()
@click.argument('repo')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.option('--token', '-t', help='GitHub API token (or set GITHUB_TOKEN env var)')
def repo(repo, verbose, token):
    """Analyze interventions for a specific repository (format: owner/repo)."""
    console.print(f"[bold blue]Analyzing interventions for: {repo}[/bold blue]\n")
    
    parts = repo.split("/")
    if len(parts) != 2:
        console.print("[red]Invalid repo format. Use: owner/repo[/red]")
        return
    
    owner, repo_name = parts
    
    github_token = token or os.getenv("GITHUB_TOKEN")
    orchestrator = CatacombOrchestrator(github_token)
    
    with console.status("[bold green]Analyzing repository..."):
        result = orchestrator.analyze_repo(owner, repo_name)
    
    if "error" in result:
        console.print(f"[red]Error: {result['error']}[/red]")
        return
    
    # Display results
    console.print(orchestrator.format_output([result], verbose=verbose))
    
    # Detailed breakdown
    if verbose:
        analysis = result.get("analysis", {})
        console.print("\n[bold]Detailed Analysis:[/bold]")
        
        # Evidence layer
        console.print("\n[cyan]Evidence Layer:[/cyan]")
        evidence = analysis.get("evidence", {})
        for layer_name, layer_data in evidence.items():
            console.print(f"  {layer_name}: {layer_data.get('score', 0):.1f}/100")
        
        # Opportunity layer
        console.print("\n[cyan]Opportunity Layer:[/cyan]")
        opportunity = analysis.get("opportunity", {})
        for layer_name, layer_data in opportunity.items():
            console.print(f"  {layer_name}: {layer_data.get('score', 0):.1f}/100")
        
        # All intervention paths
        console.print("\n[cyan]All Intervention Paths:[/cyan]")
        strategy = analysis.get("strategy", {})
        for path in strategy.get("intervention_paths", []):
            console.print(f"  - {path.get('name', 'N/A')}: {path.get('intervention_score', 0):.1f} ({path.get('effort_days', 0)} days, {path.get('probability', 0):.0%} prob, {path.get('upside', 0):.0%} upside)")


if __name__ == "__main__":
    cli()
