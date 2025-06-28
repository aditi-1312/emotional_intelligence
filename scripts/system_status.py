#!/usr/bin/env python3
"""
System Status Checker for Emotional Intelligence System
Provides comprehensive status information and health checks
"""

import sys
import os
import time
import platform
import json
from datetime import datetime
import subprocess

# Add src to path
sys.path.append('src')

def get_system_info():
    """Get basic system information"""
    info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'hostname': platform.node(),
        'timestamp': datetime.now().isoformat()
    }
    return info

def get_python_packages():
    """Get installed Python packages"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                              capture_output=True, text=True)
        packages = json.loads(result.stdout)
        return {pkg['name']: pkg['version'] for pkg in packages}
    except:
        return {}

def check_directories():
    """Check if required directories exist"""
    required_dirs = ['data', 'output', 'models', 'logs', 'src']
    status = {}
    
    for dir_name in required_dirs:
        status[dir_name] = {
            'exists': os.path.exists(dir_name),
            'writable': os.access(dir_name, os.W_OK) if os.path.exists(dir_name) else False,
            'size': len(os.listdir(dir_name)) if os.path.exists(dir_name) else 0
        }
    
    return status

def check_files():
    """Check if required files exist"""
    required_files = [
        'app.py', 'api.py', 'train_models.py', 'config.py', 
        'requirements.txt', 'README.md', 'Dockerfile', 'docker-compose.yml',
        'src/__init__.py', 'src/data_processor.py', 'src/models.py', 'src/utils.py'
    ]
    
    status = {}
    for file_name in required_files:
        status[file_name] = {
            'exists': os.path.exists(file_name),
            'size': os.path.getsize(file_name) if os.path.exists(file_name) else 0,
            'readable': os.access(file_name, os.R_OK) if os.path.exists(file_name) else False
        }
    
    return status

def test_imports():
    """Test all required imports"""
    imports_to_test = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('sklearn', 'sklearn'),
        ('streamlit', 'st'),
        ('plotly.express', 'px'),
        ('plotly.graph_objects', 'go'),
        ('matplotlib.pyplot', 'plt'),
        ('seaborn', 'sns'),
        ('wordcloud', 'WordCloud'),
        ('PIL', 'PIL'),
        ('flask', 'flask')
    ]
    
    results = {}
    for module, alias in imports_to_test:
        try:
            exec(f"import {module} as {alias}")
            results[module] = {'status': 'success', 'error': None}
        except Exception as e:
            results[module] = {'status': 'failed', 'error': str(e)}
    
    return results

def test_custom_modules():
    """Test custom module imports"""
    modules_to_test = [
        'src.data_processor',
        'src.models', 
        'src.utils'
    ]
    
    results = {}
    for module in modules_to_test:
        try:
            __import__(module)
            results[module] = {'status': 'success', 'error': None}
        except Exception as e:
            results[module] = {'status': 'failed', 'error': str(e)}
    
    return results

def test_functionality():
    """Test core functionality"""
    results = {}
    
    # Test text processing
    try:
        from src.data_processor import AdvancedTextProcessor
        processor = AdvancedTextProcessor()
        test_text = "I'm feeling happy today!"
        cleaned = processor.clean_text(test_text)
        features = processor.extract_text_features(test_text)
        results['text_processing'] = {
            'status': 'success',
            'cleaned_text': cleaned,
            'features_count': len(features)
        }
    except Exception as e:
        results['text_processing'] = {'status': 'failed', 'error': str(e)}
    
    # Test emotion analysis
    try:
        from src.models import AdvancedEmotionAnalyzer
        analyzer = AdvancedEmotionAnalyzer()
        analysis = analyzer.analyze_text("I'm feeling really happy today!")
        results['emotion_analysis'] = {
            'status': 'success',
            'dominant_emotion': analysis['dominant_emotion'],
            'confidence': analysis['confidence']
        }
    except Exception as e:
        results['emotion_analysis'] = {'status': 'failed', 'error': str(e)}
    
    # Test visualization
    try:
        from src.utils import VisualizationUtils, DataUtils
        data = DataUtils.generate_sample_data(n_samples=10)
        fig = VisualizationUtils.create_emotion_distribution_chart(data)
        results['visualization'] = {
            'status': 'success',
            'data_samples': len(data),
            'figure_created': fig is not None
        }
    except Exception as e:
        results['visualization'] = {'status': 'failed', 'error': str(e)}
    
    return results

def get_basic_performance_metrics():
    """Get basic system performance metrics without psutil"""
    try:
        # Get current working directory size
        total_size = 0
        file_count = 0
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except:
                    pass
        
        return {
            'project_size_bytes': total_size,
            'project_size_mb': total_size / (1024 * 1024),
            'file_count': file_count,
            'timestamp': time.time()
        }
    except:
        return {}

def check_ports():
    """Check if required ports are available"""
    ports_to_check = [5000, 8501]  # Flask API, Streamlit
    
    results = {}
    for port in ports_to_check:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            results[port] = {
                'available': result != 0,
                'status': 'free' if result != 0 else 'in_use'
            }
        except:
            results[port] = {'available': False, 'status': 'unknown'}
    
    return results

def generate_report():
    """Generate comprehensive system report"""
    print("🔍 Emotional Intelligence System - Status Report")
    print("=" * 60)
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # System information
    print("📋 SYSTEM INFORMATION")
    print("-" * 30)
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    print()
    
    # Basic performance metrics
    print("⚡ PROJECT METRICS")
    print("-" * 30)
    perf_metrics = get_basic_performance_metrics()
    if perf_metrics:
        print(f"  Project Size: {perf_metrics.get('project_size_mb', 'N/A'):.2f} MB")
        print(f"  File Count: {perf_metrics.get('file_count', 'N/A')}")
    else:
        print("  Unable to retrieve project metrics")
    print()
    
    # Directory status
    print("📁 DIRECTORY STATUS")
    print("-" * 30)
    dir_status = check_directories()
    for dir_name, status in dir_status.items():
        icon = "✅" if status['exists'] else "❌"
        print(f"  {icon} {dir_name}: {'exists' if status['exists'] else 'missing'}")
        if status['exists']:
            print(f"    - Files: {status['size']}")
            print(f"    - Writable: {'yes' if status['writable'] else 'no'}")
    print()
    
    # File status
    print("📄 FILE STATUS")
    print("-" * 30)
    file_status = check_files()
    for file_name, status in file_status.items():
        icon = "✅" if status['exists'] else "❌"
        print(f"  {icon} {file_name}: {'exists' if status['exists'] else 'missing'}")
        if status['exists']:
            print(f"    - Size: {status['size']} bytes")
    print()
    
    # Import status
    print("📦 IMPORT STATUS")
    print("-" * 30)
    import_results = test_imports()
    for module, result in import_results.items():
        icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {icon} {module}: {result['status']}")
        if result['status'] == 'failed':
            print(f"    - Error: {result['error']}")
    print()
    
    # Custom modules
    print("🔧 CUSTOM MODULES")
    print("-" * 30)
    custom_results = test_custom_modules()
    for module, result in custom_results.items():
        icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {icon} {module}: {result['status']}")
        if result['status'] == 'failed':
            print(f"    - Error: {result['error']}")
    print()
    
    # Functionality tests
    print("🧪 FUNCTIONALITY TESTS")
    print("-" * 30)
    func_results = test_functionality()
    for test_name, result in func_results.items():
        icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {icon} {test_name}: {result['status']}")
        if result['status'] == 'success':
            for key, value in result.items():
                if key != 'status':
                    print(f"    - {key}: {value}")
        else:
            print(f"    - Error: {result['error']}")
    print()
    
    # Port availability
    print("🌐 PORT AVAILABILITY")
    print("-" * 30)
    port_results = check_ports()
    for port, result in port_results.items():
        icon = "✅" if result['available'] else "❌"
        service = "Flask API" if port == 5000 else "Streamlit" if port == 8501 else f"Port {port}"
        print(f"  {icon} {service} (port {port}): {result['status']}")
    print()
    
    # Summary
    print("📊 SUMMARY")
    print("-" * 30)
    
    # Count successes and failures
    total_tests = 0
    passed_tests = 0
    
    # Count directory tests
    for status in dir_status.values():
        total_tests += 1
        if status['exists']:
            passed_tests += 1
    
    # Count file tests
    for status in file_status.values():
        total_tests += 1
        if status['exists']:
            passed_tests += 1
    
    # Count import tests
    for result in import_results.values():
        total_tests += 1
        if result['status'] == 'success':
            passed_tests += 1
    
    # Count custom module tests
    for result in custom_results.values():
        total_tests += 1
        if result['status'] == 'success':
            passed_tests += 1
    
    # Count functionality tests
    for result in func_results.values():
        total_tests += 1
        if result['status'] == 'success':
            passed_tests += 1
    
    print(f"  Total tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {total_tests - passed_tests}")
    print(f"  Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 Quick Start:")
        print("  1. python train_models.py")
        print("  2. streamlit run app.py")
        print("  3. python api.py")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please check the errors above.")
    
    return passed_tests == total_tests

def main():
    """Main function"""
    success = generate_report()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 