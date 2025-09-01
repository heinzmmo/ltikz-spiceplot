
if __name__ == "__main__":
    
    try:
        df = parse_ltspice_txt('../../sandbox/sample_data/rc/rc.txt')
        info = get_signal_info(df)
        
        print("=== LTspice File Info ===")
        print(f"Time column: {info['time_column']}")
        print(f"Voltage signals: {info['voltage_signals']}")
        print(f"Current signals: {info['current_signals']}")
        print(f"Total signals: {info['total_signals']}")
        print(f"Time range: {info['time_range'][0]:.2e} to {info['time_range'][1]:.2e}")
        print(f"Data points: {info['data_points']}")
        
        print("\n=== First few data points ===")
        print(df.head())
        
    except Exception as e:
        print(f"Error: {e}")
