#!/usr/bin/env python3
"""
Script to compare algorithm results saved in files
"""

import os
import json
import sys
from utils.result_saver import ResultSaver

def list_result_files(results_dir="algorithm_results"):
    """List all result files in the directory"""
    if not os.path.exists(results_dir):
        print(f"Results directory '{results_dir}' not found.")
        return []
    
    files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    files.sort(reverse=True)  # Most recent first
    
    return files

def display_file_info(files, results_dir="algorithm_results"):
    """Display information about available result files"""
    print("\n📁 Available Result Files:")
    print("=" * 60)
    
    for i, filename in enumerate(files, 1):
        filepath = os.path.join(results_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            algorithm = data.get("algorithm", "Unknown")
            timestamp = data.get("timestamp", "Unknown")
            summary = data.get("results", {}).get("summary", {})
            
            fitness = summary.get("final_fitness", "N/A")
            violations = summary.get("total_violations", "N/A")
            assignment_rate = summary.get("assignment_rate", 0) * 100
            
            print(f"{i:2d}. {filename}")
            print(f"    Algorithm: {algorithm}")
            print(f"    Timestamp: {timestamp}")
            print(f"    Fitness: {fitness}")
            print(f"    Violations: {violations}")
            print(f"    Assignment Rate: {assignment_rate:.1f}%")
            print()
            
        except Exception as e:
            print(f"{i:2d}. {filename} (Error reading file: {e})")
            print()

def analyze_single_result(filepath):
    """Analyze a single result file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n🔍 Analysis of: {os.path.basename(filepath)}")
        print("=" * 80)
        
        # Basic info
        algorithm = data.get("algorithm", "Unknown")
        timestamp = data.get("timestamp", "Unknown")
        params = data.get("parameters", {})
        results = data.get("results", {})
        summary = results.get("summary", {})
        
        print(f"Algorithm: {algorithm}")
        print(f"Execution Time: {timestamp}")
        print(f"Parameters: {params}")
        print()
        
        # Summary statistics
        print("📊 Summary Statistics:")
        print("-" * 40)
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        print()
        
        # Penalties breakdown
        penalties = results.get("penalties_breakdown", {})
        if penalties:
            print("⚠️  Penalties Breakdown:")
            print("-" * 40)
            total_penalty = sum(penalties.values())
            for penalty_type, value in penalties.items():
                if value > 0:
                    percentage = (value / total_penalty * 100) if total_penalty > 0 else 0
                    print(f"{penalty_type.replace('_', ' ').title()}: {value:.2f} ({percentage:.1f}%)")
            print()
        
        # Violations details
        violations = results.get("violations_detailed", {})
        if violations:
            print("🚨 Violations Details:")
            print("-" * 40)
            for violation_type, violation_list in violations.items():
                if violation_list:
                    print(f"{violation_type.replace('_', ' ').title()}: {len(violation_list)} occurrences")
                    for i, violation in enumerate(violation_list[:3], 1):  # Show first 3
                        print(f"  {i}. {violation}")
                    if len(violation_list) > 3:
                        print(f"  ... and {len(violation_list) - 3} more")
                    print()
        
        # Collaborator utilization
        utilization = results.get("collaborator_utilization", {})
        if utilization:
            print("👥 Collaborator Utilization:")
            print("-" * 40)
            for collab_id, usage in utilization.items():
                print(f"{usage['name']} ({usage['position']}): {usage['task_count']} tasks, {usage['total_days']} days")
            print()
        
        # Fitness evolution
        fitness_evolution = results.get("fitness_evolution", {})
        if fitness_evolution:
            history = fitness_evolution.get("history", [])
            if len(history) > 1:
                improvement = fitness_evolution.get("improvement", 0)
                print(f"📈 Fitness Evolution:")
                print(f"Initial: {history[0]:.2f} → Final: {history[-1]:.2f}")
                print(f"Improvement: {improvement:.2f} ({len(history)} generations)")
                print()
        
    except Exception as e:
        print(f"Error analyzing file: {e}")

def compare_two_results(file1, file2, results_dir="algorithm_results"):
    """Compare two result files"""
    filepath1 = os.path.join(results_dir, file1)
    filepath2 = os.path.join(results_dir, file2)
    
    result_saver = ResultSaver(results_dir)
    
    try:
        comparison = result_saver.compare_results(filepath1, filepath2)
        
        print(f"\n🆚 Comparison: {file1} vs {file2}")
        print("=" * 80)
        
        # Algorithm info
        alg1 = comparison["algorithms"]["algorithm_1"]
        alg2 = comparison["algorithms"]["algorithm_2"]
        print(f"Algorithms: {alg1} vs {alg2}")
        print()
        
        # Fitness comparison
        fitness_comp = comparison["fitness_comparison"]
        print("🎯 Fitness Comparison:")
        print("-" * 40)
        print(f"{alg1} Fitness: {fitness_comp['algorithm_1_fitness']:.2f}")
        print(f"{alg2} Fitness: {fitness_comp['algorithm_2_fitness']:.2f}")
        print(f"Winner: {fitness_comp['better_algorithm']}")
        print(f"Difference: {fitness_comp['fitness_difference']:.2f} ({fitness_comp['improvement_percentage']:.1f}%)")
        print()
        
        # Violations comparison
        violations_comp = comparison["violations_comparison"]
        print("🚨 Violations Comparison:")
        print("-" * 40)
        print(f"{alg1} Violations: {violations_comp['algorithm_1_violations']}")
        print(f"{alg2} Violations: {violations_comp['algorithm_2_violations']}")
        print(f"Fewer Violations: {violations_comp['better_algorithm']}")
        print()
        
        # Assignment comparison
        assignment_comp = comparison["assignment_comparison"]
        print("📋 Assignment Comparison:")
        print("-" * 40)
        print(f"{alg1} Assignment Rate: {assignment_comp['algorithm_1_rate']:.1%}")
        print(f"{alg2} Assignment Rate: {assignment_comp['algorithm_2_rate']:.1%}")
        print(f"Both Complete: {'Yes' if assignment_comp['both_complete'] else 'No'}")
        print()
        
    except Exception as e:
        print(f"Error comparing files: {e}")

def main():
    results_dir = "algorithm_results"
    files = list_result_files(results_dir)
    
    if not files:
        print("No result files found. Run some algorithms first!")
        return
    
    while True:
        print("\n🤖 Algorithm Results Analyzer")
        print("=" * 50)
        print("1. List all result files")
        print("2. Analyze single result")
        print("3. Compare two results")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            display_file_info(files, results_dir)
            
        elif choice == "2":
            display_file_info(files, results_dir)
            try:
                file_num = int(input(f"\nSelect file number (1-{len(files)}): "))
                if 1 <= file_num <= len(files):
                    filepath = os.path.join(results_dir, files[file_num - 1])
                    analyze_single_result(filepath)
                else:
                    print("Invalid file number!")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "3":
            display_file_info(files, results_dir)
            try:
                file1_num = int(input(f"\nSelect first file (1-{len(files)}): "))
                file2_num = int(input(f"Select second file (1-{len(files)}): "))
                
                if 1 <= file1_num <= len(files) and 1 <= file2_num <= len(files):
                    if file1_num != file2_num:
                        compare_two_results(files[file1_num - 1], files[file2_num - 1], results_dir)
                    else:
                        print("Please select different files!")
                else:
                    print("Invalid file numbers!")
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == "4":
            print("Goodbye! 👋")
            break
            
        else:
            print("Invalid option! Please select 1-4.")

if __name__ == "__main__":
    main()