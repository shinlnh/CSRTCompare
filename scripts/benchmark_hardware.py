"""
Hardware Benchmark Script for Object Trackers
Measures CPU, RAM, GPU usage, FPS, and latency for different trackers
"""
import cv2
import numpy as np
import time
import psutil
import os
import sys
from pathlib import Path
import json
import pandas as pd
from typing import Dict, List, Tuple
import traceback

# Add trackers directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'trackers'))

# Try to import GPUtil (optional)
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("Warning: GPUtil not available. GPU metrics will not be collected.")

# Import tracker wrappers
from csrt_wrapper import CSRTWrapper
from ostrack_wrapper import OSTrackWrapper
from siamrpn_wrapper import SiamRPNWrapper
from dimp_wrapper import DIMPWrapper

class HardwareBenchmark:
    """Benchmark trackers with hardware metrics"""
    
    def __init__(self, video_path: str, output_dir: str = "../results"):
        self.video_path = video_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize trackers
        self.trackers = {
            'CSRT': CSRTWrapper(),
            'OSTrack': OSTrackWrapper(),
            'SiamRPN++': SiamRPNWrapper(),
            'DiMP': DIMPWrapper()
        }
        
        # Process info
        self.process = psutil.Process(os.getpid())
        
    def measure_hardware(self) -> Dict:
        """Measure current hardware usage"""
        metrics = {
            'cpu_percent': self.process.cpu_percent(interval=0.01),
            'ram_mb': self.process.memory_info().rss / 1024 / 1024,
            'ram_percent': self.process.memory_percent()
        }
        
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    metrics['gpu_util'] = gpu.load * 100
                    metrics['gpu_memory_mb'] = gpu.memoryUsed
                    metrics['gpu_memory_percent'] = (gpu.memoryUsed / gpu.memoryTotal) * 100
                    metrics['gpu_temp'] = gpu.temperature
                else:
                    metrics.update({
                        'gpu_util': 0,
                        'gpu_memory_mb': 0,
                        'gpu_memory_percent': 0,
                        'gpu_temp': 0
                    })
            except Exception as e:
                print(f"GPU metrics error: {e}")
                metrics.update({
                    'gpu_util': 0,
                    'gpu_memory_mb': 0,
                    'gpu_memory_percent': 0,
                    'gpu_temp': 0
                })
        else:
            metrics.update({
                'gpu_util': 0,
                'gpu_memory_mb': 0,
                'gpu_memory_percent': 0,
                'gpu_temp': 0
            })
            
        return metrics
    
    def benchmark_tracker(self, tracker_name: str, num_frames: int = 300) -> Dict:
        """
        Benchmark a single tracker
        Args:
            tracker_name: Name of tracker to benchmark
            num_frames: Number of frames to process
        Returns:
            Dictionary with benchmark results
        """
        print(f"\n{'='*60}")
        print(f"Benchmarking {tracker_name}...")
        print(f"{'='*60}")
        
        tracker = self.trackers[tracker_name]
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"Error: Cannot open video {self.video_path}")
            return None
        
        # Read first frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read first frame")
            return None
        
        # Manual bounding box selection or use default
        # For automation, we'll use center box
        h, w = frame.shape[:2]
        bbox = (w//4, h//4, w//2, h//2)  # Center box
        
        print(f"Initializing tracker with bbox: {bbox}")
        tracker.init(frame, bbox)
        
        # Metrics storage
        frame_times = []
        cpu_usage = []
        ram_usage = []
        gpu_usage = []
        gpu_memory = []
        latencies = []
        
        # Baseline hardware
        baseline = self.measure_hardware()
        print(f"Baseline - CPU: {baseline['cpu_percent']:.1f}%, RAM: {baseline['ram_mb']:.1f}MB")
        
        frame_count = 0
        max_frames = min(num_frames, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        
        print(f"Processing {max_frames} frames...")
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Measure tracking time and hardware
            start_time = time.perf_counter()
            hw_before = self.measure_hardware()
            
            success, bbox = tracker.update(frame)
            
            end_time = time.perf_counter()
            hw_after = self.measure_hardware()
            
            # Calculate metrics
            latency = (end_time - start_time) * 1000  # ms
            latencies.append(latency)
            frame_times.append(end_time - start_time)
            
            # Hardware metrics (delta from baseline)
            cpu_usage.append(hw_after['cpu_percent'])
            ram_usage.append(hw_after['ram_mb'] - baseline['ram_mb'])
            gpu_usage.append(hw_after['gpu_util'])
            gpu_memory.append(hw_after['gpu_memory_mb'])
            
            frame_count += 1
            
            if frame_count % 50 == 0:
                avg_fps = frame_count / sum(frame_times)
                print(f"Frame {frame_count}/{max_frames} - FPS: {avg_fps:.1f}, "
                      f"Latency: {latency:.1f}ms, CPU: {hw_after['cpu_percent']:.1f}%")
        
        cap.release()
        
        # Calculate summary statistics
        results = {
            'tracker': tracker_name,
            'frames_processed': frame_count,
            'avg_fps': frame_count / sum(frame_times) if frame_times else 0,
            'min_fps': 1.0 / max(frame_times) if frame_times else 0,
            'max_fps': 1.0 / min(frame_times) if frame_times else 0,
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
            'baseline_ram_mb': baseline['ram_mb'],
            'latency_variance': np.var(latencies)
        }
        
        # Detailed frame-by-frame data
        results['frame_data'] = {
            'latencies': latencies,
            'cpu_usage': cpu_usage,
            'ram_usage': ram_usage,
            'gpu_usage': gpu_usage,
            'gpu_memory': gpu_memory
        }
        
        print(f"\n{tracker_name} Results:")
        print(f"  Avg FPS: {results['avg_fps']:.2f}")
        print(f"  Avg Latency: {results['avg_latency_ms']:.2f}ms (±{results['std_latency_ms']:.2f})")
        print(f"  P95 Latency: {results['p95_latency_ms']:.2f}ms")
        print(f"  Avg CPU: {results['avg_cpu_percent']:.1f}%")
        print(f"  Avg RAM: {results['avg_ram_mb']:.1f}MB")
        print(f"  Avg GPU: {results['avg_gpu_util']:.1f}%")
        print(f"  Avg GPU Memory: {results['avg_gpu_memory_mb']:.1f}MB")
        
        return results
    
    def run_all_benchmarks(self, num_frames: int = 300):
        """Run benchmarks for all trackers"""
        all_results = {}
        
        for tracker_name in self.trackers.keys():
            try:
                result = self.benchmark_tracker(tracker_name, num_frames)
                if result:
                    all_results[tracker_name] = result
                    
                # Cool down between trackers
                print("\nCooling down for 3 seconds...")
                time.sleep(3)
                
            except Exception as e:
                print(f"Error benchmarking {tracker_name}: {e}")
                traceback.print_exc()
        
        # Save results
        self.save_results(all_results)
        return all_results
    
    def save_results(self, results: Dict):
        """Save benchmark results to files"""
        
        # Summary table
        summary_data = []
        for tracker_name, result in results.items():
            summary_data.append({
                'Tracker': result['tracker'],
                'Avg_FPS': result['avg_fps'],
                'Min_FPS': result['min_fps'],
                'Avg_Latency_ms': result['avg_latency_ms'],
                'Std_Latency_ms': result['std_latency_ms'],
                'P95_Latency_ms': result['p95_latency_ms'],
                'P99_Latency_ms': result['p99_latency_ms'],
                'Latency_Variance': result['latency_variance'],
                'Avg_CPU_%': result['avg_cpu_percent'],
                'Max_CPU_%': result['max_cpu_percent'],
                'Avg_RAM_MB': result['avg_ram_mb'],
                'Max_RAM_MB': result['max_ram_mb'],
                'Avg_GPU_%': result['avg_gpu_util'],
                'Max_GPU_%': result['max_gpu_util'],
                'Avg_GPU_Memory_MB': result['avg_gpu_memory_mb'],
                'Max_GPU_Memory_MB': result['max_gpu_memory_mb']
            })
        
        df_summary = pd.DataFrame(summary_data)
        summary_path = self.output_dir / 'hardware_benchmark_summary.csv'
        df_summary.to_csv(summary_path, index=False)
        print(f"\nSummary saved to: {summary_path}")
        
        # Full JSON results
        # Remove frame_data for JSON (too large)
        json_results = {}
        for name, result in results.items():
            json_results[name] = {k: v for k, v in result.items() if k != 'frame_data'}
        
        json_path = self.output_dir / 'hardware_benchmark_full.json'
        with open(json_path, 'w') as f:
            json.dump(json_results, f, indent=2)
        print(f"Full results saved to: {json_path}")
        
        # Frame-by-frame data for MATLAB
        for tracker_name, result in results.items():
            if 'frame_data' in result:
                frame_df = pd.DataFrame(result['frame_data'])
                frame_df['tracker'] = tracker_name
                frame_df['frame_number'] = range(len(frame_df))
                
                frame_path = self.output_dir / f'{tracker_name}_frame_data.csv'
                frame_df.to_csv(frame_path, index=False)
                print(f"{tracker_name} frame data saved to: {frame_path}")
        
        print(f"\n{'='*60}")
        print("BENCHMARK SUMMARY")
        print(f"{'='*60}")
        print(df_summary.to_string(index=False))
        print(f"{'='*60}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Benchmark object trackers')
    parser.add_argument('--video', type=str, default='../test_videos/test.mp4',
                        help='Path to test video')
    parser.add_argument('--frames', type=int, default=300,
                        help='Number of frames to process')
    parser.add_argument('--output', type=str, default='../results',
                        help='Output directory for results')
    
    args = parser.parse_args()
    
    # Check if video exists, if not create test video
    if not Path(args.video).exists():
        print(f"Video not found: {args.video}")
        print("Creating synthetic test video...")
        create_test_video(args.video)
    
    benchmark = HardwareBenchmark(args.video, args.output)
    results = benchmark.run_all_benchmarks(args.frames)
    
    print("\nBenchmark complete! Results saved to:", args.output)
    print("\nYou can now import these CSV files into MATLAB for analysis.")

def create_test_video(output_path: str, num_frames: int = 500):
    """Create a synthetic test video with moving object"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (640, 480))
    
    for i in range(num_frames):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (50, 50, 50)  # Gray background
        
        # Moving rectangle
        x = int(100 + i * 0.5) % 540
        y = 200 + int(50 * np.sin(i * 0.05))
        cv2.rectangle(frame, (x, y), (x + 100, y + 80), (0, 255, 0), -1)
        
        # Add noise
        noise = np.random.randint(0, 20, frame.shape, dtype=np.uint8)
        frame = cv2.add(frame, noise)
        
        out.write(frame)
    
    out.release()
    print(f"Test video created: {output_path}")

if __name__ == '__main__':
    main()
