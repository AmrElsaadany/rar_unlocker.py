import sys
import os
import shutil

# RAR format signatures
RAR4_SIGNATURE = b'Rar!\x1a\x07\x00'
RAR5_SIGNATURE = b'Rar!\x1a\x07\x01\x00'

def create_backup(file_path):
    """Create a backup copy of the RAR file before modification."""
    backup_path = file_path + '.backup'
    
    if os.path.exists(backup_path):
        print(f"[!] Backup already exists: {backup_path}")
        response = input("[?] Do you want to overwrite the existing backup? (yes/no): ").strip().lower()
        if response != 'yes':
            print("[-] Backup creation cancelled.")
            return None
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"[+] Backup created successfully: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"[-] Error creating backup: {e}")
        return None

def unlock_rar(file_path, apply_fix=False):
    if not os.path.exists(file_path):
        print(f"[-] Error: File '{file_path}' not found.")
        return

    with open(file_path, 'rb+') as f:
        # Check Magic Number
        file_head = f.read(8)
        
        # --- RAR4 Processing ---
        if file_head.startswith(RAR4_SIGNATURE):
            print("[+] Format detected: RAR 4.x")
            # In RAR4, Main Header immediately follows the 7-byte signature.
            # Main Header Type is typically 0x73. Let's inspect the block header:
            f.seek(7)
            head_crc = f.read(2)
            head_type = f.read(1)
            head_flags = int.from_bytes(f.read(2), byteorder='little')
            
            if head_type == b'\x73':
                # Flag bit 0x0004 represents the volume/archive lock attribute
                is_locked = bool(head_flags & 0x0004)
                print(f"[!] Current Status: {'LOCKED' if is_locked else 'UNLOCKED'}")
                
                if is_locked and apply_fix:
                    new_flags = head_flags & ~0x0004  # Clear the 0x0004 bit
                    f.seek(7 + 2 + 1)  # Navigate to head_flags position
                    f.write(new_flags.to_bytes(2, byteorder='little'))
                    print("[+] Success: Archive lock attribute stripped down!")
            else:
                print("[-] Could not isolate the Main Header block layout.")

        # --- RAR5 Processing ---
        elif file_head == RAR5_SIGNATURE:
            print("[+] Format detected: RAR 5.x")
            # In RAR5, blocks are variable size encoded using VINTs.
            # Main Archive header follows the 8-byte signature.
            f.seek(8)
            # Read enough bytes to parse the main archive property flags
            block_bytes = f.read(20)
            
            # RAR5 Main Header Type is 1. Let's find the header structure
            # A typical structural parsing handles VINT lengths. 
            # Simplified look-ahead for the lock bit flags (typically at an offset):
            print("[!] RAR5 parsing depends on VINT field offsets.")
            print("[*] For fully complex flag manipulation, re-archiving via CLI tool 'rar' is cleaner on Linux.")
            
        else:
            print("[-] Error: Not a valid RAR archive file.")

def main():
    """Interactive main function to guide user through the process."""
    print("=" * 60)
    print("         RAR UNLOCKER - Interactive Mode")
    print("=" * 60)
    print()
    
    # Step 1: Get input file path
    while True:
        target_file = input("[?] Enter the path to the RAR file to be unlocked: ").strip()
        
        if not target_file:
            print("[-] File path cannot be empty. Please try again.")
            continue
        
        if not os.path.exists(target_file):
            print(f"[-] File '{target_file}' not found. Please check the path and try again.")
            continue
        
        if not target_file.lower().endswith('.rar'):
            response = input("[!] File doesn't have .rar extension. Continue anyway? (yes/no): ").strip().lower()
            if response != 'yes':
                print("[-] File selection cancelled.")
                continue
        
        print(f"[+] File selected: {target_file}")
        break
    
    print()
    
    # Step 2: Ask about backup
    while True:
        backup_response = input("[?] Do you want to create a backup before proceeding? (yes/no): ").strip().lower()
        
        if backup_response == 'yes':
            backup_path = create_backup(target_file)
            if backup_path is None:
                retry = input("[?] Failed to create backup. Continue without backup? (yes/no): ").strip().lower()
                if retry == 'yes':
                    print("[!] Proceeding without backup...")
                    break
                else:
                    print("[-] Operation cancelled.")
                    return
            else:
                break
        elif backup_response == 'no':
            warning = input("[!] WARNING: No backup will be created. Continue? (yes/no): ").strip().lower()
            if warning == 'yes':
                print("[!] Proceeding without backup...")
                break
            else:
                print("[-] Operation cancelled.")
                return
        else:
            print("[-] Invalid response. Please enter 'yes' or 'no'.")
            continue
    
    print()
    
    # Step 3: Check archive status
    print("[*] Checking archive status...")
    print()
    unlock_rar(target_file, apply_fix=False)
    
    print()
    
    # Step 4: Ask if user wants to unlock
    while True:
        unlock_response = input("[?] Do you want to unlock this archive? (yes/no): ").strip().lower()
        
        if unlock_response == 'yes':
            print("[*] Unlocking archive...")
            unlock_rar(target_file, apply_fix=True)
            print("[+] Process completed!")
            break
        elif unlock_response == 'no':
            print("[!] Archive was not modified.")
            break
        else:
            print("[-] Invalid response. Please enter 'yes' or 'no'.")
            continue
    
    print()
    print("=" * 60)
    print("                  Thank you for using RAR Unlocker!")
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Legacy command-line mode
        target_file = sys.argv[1]
        fix_flag = len(sys.argv) > 2 and sys.argv[2] == '--unlock'
        unlock_rar(target_file, apply_fix=fix_flag)
    else:
        # Interactive mode
        main()
