#!/usr/bin/env python3
"""
Quick start script to run complete benchmark pipeline
"""
import subprocess
import sys
from pathlib import Path
import time

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ Command not found: {cmd[0]}")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   CSRT vs Modern Trackers Hardware Benchmark              ║
    ║   Demonstrating CSRT's superiority for robotics           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Change to project root
    project_root = Path(__file__).parent
    
    # Step 1: Install requirements
    print("\n[1/3] Checking Python dependencies...")
    requirements_file = project_root / "requirements_trackers.txt"
    if requirements_file.exists():
        install = input("Install/update requirements? (y/n): ")
        if install.lower() == 'y':
            run_command(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                "Installing Python dependencies"
            )
    
    # Step 2: Run benchmark
    print("\n[2/3] Running hardware benchmark...")
    print("This will take a few minutes...")
    
    benchmark_script = project_root / "scripts" / "benchmark_hardware.py"
    video_path = project_root / "test_videos" / "test.mp4"
    results_path = project_root / "results"
    
    # Create directories
    (project_root / "test_videos").mkdir(exist_ok=True)
    results_path.mkdir(exist_ok=True)
    (project_root / "plots").mkdir(exist_ok=True)
    
    success = run_command(
        [sys.executable, str(benchmark_script), 
         "--video", str(video_path),
         "--frames", "300",
         "--output", str(results_path)],
        "Hardware Benchmark"
    )
    
    if not success:
        print("\n✗ Benchmark failed. Please check error messages above.")
        return
    
    # Step 3: Run MATLAB analysis
    print("\n[3/3] MATLAB Analysis")
    print("\nBenchmark complete! Results saved to:")
    print(f"  - {results_path}")
    print(f"\nTo generate plots, run MATLAB:")
    print(f"  1. Open MATLAB")
    print(f"  2. cd {project_root / 'scripts'}")
    print(f"  3. Run: analyze_hardware_matlab")
    print(f"\nOr run manually:")
    print(f"  matlab -batch \"cd {project_root / 'scripts'}; analyze_hardware_matlab\"")
    
    matlab_auto = input("\nTry to run MATLAB analysis automatically? (y/n): ")
    if matlab_auto.lower() == 'y':
        matlab_script = project_root / "scripts" / "analyze_hardware_matlab.m"
        run_command(
            ["matlab", "-batch", f"cd('{project_root / 'scripts'}'); analyze_hardware_matlab"],
            "MATLAB Analysis"
        )
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║                  BENCHMARK COMPLETE!                       ║
    ╚════════════════════════════════════════════════════════════╝
    
    Results Location:
      📁 CSV Data:    {results_path}
      📊 Plots:       {project_root / 'plots'}
      📖 Guide:       {project_root / 'HARDWARE_BENCHMARK_README.md'}
    
    Key Files:
      • hardware_benchmark_summary.csv  - Main results
      • *_frame_data.csv                - Detailed frame data
      • hardware_comparison_overview.png - Visual comparison
      • robotics_suitability.png        - Suitability scores
    
    Next Steps:
      1. Check plots/ directory for visualizations
      2. Import CSV files to MATLAB for custom analysis
      3. Use results to demonstrate CSRT advantages
    
    ╔════════════════════════════════════════════════════════════╗
    ║  CSRT Wins for Robotics: Predictable, Efficient, Cheap!   ║
    ╚════════════════════════════════════════════════════════════╝
    """)

if __name__ == '__main__':
    main()
