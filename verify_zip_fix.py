import os
import shutil
import zipfile
import converter_utils

def test_repackaging_robustness():
    print("--- Running Repackaging Robustness Test ---")
    
    # 1. Setup temp environment
    test_dir = "test_robust_packaging"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Create some dummy files
    os.makedirs(os.path.join(test_dir, "content"))
    for i in range(10):
        with open(os.path.join(test_dir, "content", f"file{i}.txt"), "w") as f:
            f.write(f"Content {i}")
            
    # Create folders that SHOULD be skipped
    os.makedirs(os.path.join(test_dir, "venv"))
    with open(os.path.join(test_dir, "venv", "secret.txt"), "w") as f:
        f.write("Should not be zipped")
        
    os.makedirs(os.path.join(test_dir, "__pycache__"))
    
    # 2. Output path with DIFFERENT CASING (Windows test)
    # If the real path is test_robust_packaging, we save to TEST_ROBUST_PACKAGING\OUT.imscc
    output_path = os.path.join(test_dir, "REPACKAGED.IMSCC")
    
    # Logging callback
    logs = []
    def my_log(msg):
        logs.append(msg)
        print(f"   [CALLBACK] {msg}")

    # 3. Call the function
    print(f"Repackaging {test_dir} into {output_path}...")
    success, msg = converter_utils.create_course_package(test_dir, output_path, log_func=my_log)
    
    if not success:
        print(f"FAILED: {msg}")
        return
    
    print(f"Success: {msg}")
    
    # 4. Verify ZIP
    try:
        with zipfile.ZipFile(output_path, 'r') as z:
            file_list = z.namelist()
            print(f"Files in ZIP ({len(file_list)} total): {file_list[:10]}...")
            
            # Check self-exclusion (Case-Insensitive)
            if any(f.lower() == "repackaged.imscc" for f in file_list):
                 print("FAILED: Output file was included in the ZIP!")
            else:
                 print("Self-exclusion check (Case-Insensitive) PASSED.")
            
            # Check folder exclusion
            if any("venv" in f for f in file_list):
                 print("FAILED: 'venv' folder was included!")
            else:
                 print("Directory exclusion check (venv) PASSED.")
                 
            if len(file_list) == 10: # Only the 10 files in content/ should be there
                 print("File count check PASSED.")
            else:
                 print(f"WARNING: Unexpected file count: {len(file_list)}")

    except Exception as e:
        print(f"FAILED: Could not open ZIP: {e}")
    finally:
        # Cleanup
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print("Cleanup complete.")

if __name__ == "__main__":
    test_repackaging_robustness()
