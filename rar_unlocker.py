import sys
import os

# RAR format signatures
RAR4_SIGNATURE = b'Rar!\x1a\x07\x00'
RAR5_SIGNATURE = b'Rar!\x1a\x07\x01\x00'

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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  To view status: python rar_unlocker.py archive.rar")
        print("  To unlock:      python rar_unlocker.py archive.rar --unlock")
        sys.exit(1)

    target_file = sys.argv[1]
    fix_flag = len(sys.argv) > 2 and sys.argv[2] == '--unlock'
    
    unlock_rar(target_file, apply_fix=fix_flag)
