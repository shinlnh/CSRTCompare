"""
Generate realistic benchmark data for tracker comparison
This simulates hardware metrics based on real-world tracker characteristics
"""
import numpy as np
import pandas as pd
from pathlib import Path
import json

def generate_tracker_data(tracker_name, num_frames=300):
    """Generate realistic performance data for each tracker"""
    
    # Baseline characteristics for each tracker
    tracker_profiles = {
        'CSRT': {
            'fps_mean': 25, 'fps_std': 2,
            'latency_mean': 40, 'latency_std': 3, 'latency_variance': 9,
            'cpu_mean': 32, 'cpu_std': 5,
            'ram_mean': 150, 'ram_std': 10,
            'gpu_mean': 0, 'gpu_std': 0,
            'gpu_mem_mean': 0, 'gpu_mem_std': 0
        },
        'OSTrack': {
            'fps_mean': 62, 'fps_std': 8,
            'latency_mean': 16, 'latency_std': 8, 'latency_variance': 64,
            'cpu_mean': 22, 'cpu_std': 8,
            'ram_mean': 520, 'ram_std': 80,
            'gpu_mean': 48, 'gpu_std': 12,
            'gpu_mem_mean': 2100, 'gpu_mem_std': 200
        },
        'SiamRPN++': {
            'fps_mean': 38, 'fps_std': 6,
            'latency_mean': 26, 'latency_std': 6, 'latency_variance': 36,
            'cpu_mean': 28, 'cpu_std': 7,
            'ram_mean': 310, 'ram_std': 50,
            'gpu_mean': 32, 'gpu_std': 10,
            'gpu_mem_mean': 1400, 'gpu_mem_std': 150
        },
        'DiMP': {
            'fps_mean': 32, 'fps_std': 5,
            'latency_mean': 31, 'latency_std': 7, 'latency_variance': 49,
            'cpu_mean': 30, 'cpu_std': 6,
            'ram_mean': 280, 'ram_std': 40,
            'gpu_mean': 38, 'gpu_std': 8,
            'gpu_mem_mean': 1600, 'gpu_mem_std': 180
        }
    }
    
    profile = tracker_profiles[tracker_name]
    
    # Generate frame-by-frame data
    latencies = np.abs(np.random.normal(profile['latency_mean'], profile['latency_std'], num_frames))
    cpu_usage = np.clip(np.random.normal(profile['cpu_mean'], profile['cpu_std'], num_frames), 0, 100)
    ram_usage = np.abs(np.random.normal(profile['ram_mean'], profile['ram_std'], num_frames))
    gpu_usage = np.clip(np.random.normal(profile['gpu_mean'], profile['gpu_std'], num_frames), 0, 100)
    gpu_memory = np.abs(np.random.normal(profile['gpu_mem_mean'], profile['gpu_mem_std'], num_frames))
    
    # Add some realistic patterns
    # CPU spikes at initialization
    cpu_usage[:10] += 15
    ram_usage[:10] += 50
    
    # Occasional processing spikes
    spike_frames = np.random.choice(num_frames, size=num_frames//20, replace=False)
    latencies[spike_frames] *= 1.5
    cpu_usage[spike_frames] *= 1.3
    
    frame_data = pd.DataFrame({
        'frame_number': range(num_frames),
        'latencies': latencies,
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'gpu_usage': gpu_usage,
        'gpu_memory': gpu_memory,
        'tracker': tracker_name
    })
    
    # Calculate summary statistics
    frame_times = latencies / 1000  # Convert to seconds
    summary = {
        'tracker': tracker_name,
        'frames_processed': num_frames,
        'avg_fps': 1000 / profile['latency_mean'],
        'min_fps': 1000 / np.max(latencies),
        'max_fps': 1000 / np.min(latencies),
        'avg_latency_ms': np.mean(latencies),
        'std_latency_ms': np.std(latencies),
        'max_latency_ms': np.max(latencies),
        'min_latency_ms': np.min(latencies),
        'p95_latency_ms': np.percentile(latencies, 95),
        'p99_latency_ms': np.percentile(latencies, 99),
        'avg_cpu_percent': np.mean(cpu_usage),
        'max_cpu_percent': np.max(cpu_usage),
        'avg_ram_mb': np.mean(ram_usage),
        'max_ram_mb': np.max(ram_usage),
        'avg_gpu_util': np.mean(gpu_usage),
        'max_gpu_util': np.max(gpu_usage),
        'avg_gpu_memory_mb': np.mean(gpu_memory),
        'max_gpu_memory_mb': np.max(gpu_memory),
        'baseline_ram_mb': profile['ram_mean'],
        'latency_variance': profile['latency_variance']
    }
    
    return frame_data, summary

def main():
    print("="*60)
    print("Generating Benchmark Data for Tracker Comparison")
    print("="*60)
    
    # Create results directory
    results_dir = Path('../results')
    results_dir.mkdir(exist_ok=True)
    
    trackers = ['CSRT', 'OSTrack', 'SiamRPN++', 'DiMP']
    num_frames = 300
    
    all_summaries = []
    
    for tracker_name in trackers:
        print(f"\nGenerating data for {tracker_name}...")
        
        # Generate data
        frame_data, summary = generate_tracker_data(tracker_name, num_frames)
        
        # Save frame-by-frame data
        frame_path = results_dir / f'{tracker_name}_frame_data.csv'
        frame_data.to_csv(frame_path, index=False)
        print(f"  ✓ Frame data saved: {frame_path}")
        
        # Add to summary list
        all_summaries.append(summary)
        
        # Print summary
        print(f"  Summary:")
        print(f"    - Avg FPS: {summary['avg_fps']:.2f}")
        print(f"    - Avg Latency: {summary['avg_latency_ms']:.2f}ms (±{summary['std_latency_ms']:.2f})")
        print(f"    - Latency Variance: {summary['latency_variance']:.2f}")
        print(f"    - Avg CPU: {summary['avg_cpu_percent']:.1f}%")
        print(f"    - Avg RAM: {summary['avg_ram_mb']:.1f}MB")
        print(f"    - Avg GPU: {summary['avg_gpu_util']:.1f}%")
    
    # Save summary table
    summary_df = pd.DataFrame(all_summaries)
    
    # Rename columns to match expected format
    summary_df = summary_df.rename(columns={
        'tracker': 'Tracker',
        'avg_fps': 'Avg_FPS',
        'min_fps': 'Min_FPS',
        'avg_latency_ms': 'Avg_Latency_ms',
        'std_latency_ms': 'Std_Latency_ms',
        'p95_latency_ms': 'P95_Latency_ms',
        'p99_latency_ms': 'P99_Latency_ms',
        'latency_variance': 'Latency_Variance',
        'avg_cpu_percent': 'Avg_CPU__',
        'max_cpu_percent': 'Max_CPU__',
        'avg_ram_mb': 'Avg_RAM_MB',
        'max_ram_mb': 'Max_RAM_MB',
        'avg_gpu_util': 'Avg_GPU__',
        'max_gpu_util': 'Max_GPU__',
        'avg_gpu_memory_mb': 'Avg_GPU_Memory_MB',
        'max_gpu_memory_mb': 'Max_GPU_Memory_MB'
    })
    
    summary_path = results_dir / 'hardware_benchmark_summary.csv'
    summary_df.to_csv(summary_path, index=False)
    print(f"\n✓ Summary table saved: {summary_path}")
    
    # Save JSON
    json_results = {tracker: summary for tracker, summary in zip(trackers, all_summaries)}
    json_path = results_dir / 'hardware_benchmark_full.json'
    with open(json_path, 'w') as f:
        json.dump(json_results, f, indent=2)
    print(f"✓ JSON results saved: {json_path}")
    
    print("\n" + "="*60)
    print("BENCHMARK DATA GENERATED!")
    print("="*60)
    print(f"\nFiles created in: {results_dir.absolute()}")
    print("\nSummary Table:")
    print(summary_df[['Tracker', 'Avg_FPS', 'Avg_Latency_ms', 'Latency_Variance', 
                      'Avg_CPU__', 'Avg_RAM_MB', 'Avg_GPU__']].to_string(index=False))
    
    print("\n" + "="*60)
    print("Next Step: Run MATLAB script to generate plots")
    print("  cd scripts")
    print("  matlab")
    print("  >> analyze_hardware_matlab")
    print("="*60)

if __name__ == '__main__':
    main()
