#!/usr/bin/env python3
"""
LED Control - Explorer 8 UART Communication
Type 'murat' to blink the LED on the PIC16F1719

Usage: python led_control.py
"""

import serial
import serial.tools.list_ports
import time
import sys

def find_serial_port():
    """Find the MCP2221 USB-UART port"""
    ports = serial.tools.list_ports.comports()
    
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device} - {port.description}")
    
    # Try to auto-detect MCP2221
    for port in ports:
        if "MCP2221" in port.description or "usbmodem" in port.device:
            print(f"\nAuto-detected: {port.device}")
            return port.device
    
    # If not found, let user choose
    if ports:
        choice = input("\nSelect port number (or press Enter for first one): ")
        if choice.strip() == "":
            return ports[0].device
        return ports[int(choice)].device
    
    return None

def main():
    print("=" * 50)
    print("  Explorer 8 LED Control")
    print("  Type 'murat' to blink the LED")
    print("  Type 'exit' to quit")
    print("=" * 50)
    
    # Find serial port
    port = find_serial_port()
    
    if not port:
        print("Error: No serial port found!")
        print("Make sure Explorer 8 is connected via USB.")
        sys.exit(1)
    
    try:
        # Open serial connection
        ser = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1
        )
        
        print(f"\nConnected to {port}")
        print("-" * 50)
        
        # Wait for PIC to initialize
        time.sleep(1)
        
        # Read any startup message from PIC
        while ser.in_waiting:
            print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'), end='')
        
        print("\nReady! Type a command and press Enter:\n")
        
        while True:
            # Get user input
            try:
                user_input = input("> ")
            except EOFError:
                break
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            # Send to PIC (with newline)
            ser.write((user_input + '\r').encode())
            
            # Wait and read response
            time.sleep(0.5)
            
            while ser.in_waiting:
                response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                print(response, end='')
            
            print()  # New line
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
