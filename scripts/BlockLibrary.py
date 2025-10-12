"""
Rhino Design Library - Block Importer
Downloads and inserts blocks from your GitHub repository
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import json
import os
import System.Net

# ========== CONFIGURATION ==========
# Replace these with your GitHub repository details
GITHUB_USER = "aarslanovic"
REPO_NAME = "AMAR.IO_WORKSHOP"
BRANCH = "main"

# Base URLs
CATALOG_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/catalog.json"
BLOCKS_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/blocks/"

# Local cache directory
CACHE_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'RhinoBlockLibrary', 'cache')


def ensure_cache_dir():
    """Create cache directory if it doesn't exist"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    return CACHE_DIR


def download_file(url, local_path):
    """Download a file from URL to local path"""
    try:
        web_client = System.Net.WebClient()
        web_client.DownloadFile(url, local_path)
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False


def load_catalog():
    """Load the catalog.json from GitHub"""
    try:
        cache_dir = ensure_cache_dir()
        catalog_cache = os.path.join(cache_dir, 'catalog.json')
        
        # Download fresh catalog
        if download_file(CATALOG_URL, catalog_cache):
            with open(catalog_cache, 'r') as f:
                catalog = json.load(f)
            return catalog
        else:
            print("Failed to download catalog")
            return None
    except Exception as e:
        print(f"Error loading catalog: {e}")
        return None


def get_blocks_by_category(catalog):
    """Organize blocks by category"""
    blocks_by_cat = {}
    for block in catalog.get('blocks', []):
        cat = block.get('category', 'uncategorized')
        if cat not in blocks_by_cat:
            blocks_by_cat[cat] = []
        blocks_by_cat[cat].append(block)
    return blocks_by_cat


def browse_and_insert():
    """Main function - browse library and insert block"""
    
    # Load catalog
    print("Loading block library...")
    catalog = load_catalog()
    
    if not catalog:
        rs.MessageBox("Failed to load block library. Check your internet connection.", 0, "Error")
        return
    
    # Get blocks organized by category
    blocks_by_cat = get_blocks_by_category(catalog)
    categories = sorted(blocks_by_cat.keys())
    
    if not categories:
        rs.MessageBox("No blocks found in library.", 0, "Error")
        return
    
    # Step 1: Choose category
    category = rs.ListBox(categories, "Select Block Category", "Block Library")
    if not category:
        return
    
    # Step 2: Choose block
    blocks_in_cat = blocks_by_cat[category]
    block_names = [f"{b['name']} - {b.get('description', '')}" for b in blocks_in_cat]
    
    selected = rs.ListBox(block_names, f"Select Block from {category.title()}", "Block Library")
    if not selected:
        return
    
    # Find the selected block
    selected_index = block_names.index(selected)
    block_info = blocks_in_cat[selected_index]
    
    # Download and insert
    insert_block(block_info)


def insert_block(block_info):
    """Download and insert a block into Rhino"""
    
    block_name = block_info['name']
    block_file = block_info['file']
    block_id = block_info.get('id', block_file.replace('/', '_').replace('.3dm', ''))
    
    print(f"Preparing to insert: {block_name}")
    
    # Check if block already exists in document
    existing_blocks = rs.BlockNames()
    if block_id in existing_blocks:
        result = rs.MessageBox(
            f"Block '{block_name}' already exists in this file.\n\nInsert another instance?",
            4 | 32,  # Yes/No + Question icon
            "Block Exists"
        )
        if result == 7:  # No
            return
        # If Yes, just insert existing block
        insert_point = rs.GetPoint("Pick insertion point")
        if insert_point:
            rs.InsertBlock(block_id, insert_point)
        return
    
    # Download block file
    cache_dir = ensure_cache_dir()
    local_file = os.path.join(cache_dir, block_file.replace('/', '_'))
    block_url = BLOCKS_BASE_URL + block_file
    
    print(f"Downloading from: {block_url}")
    
    if not download_file(block_url, local_file):
        rs.MessageBox(f"Failed to download block: {block_name}", 0, "Download Error")
        return
    
    print(f"Downloaded to: {local_file}")
    
    # Get insertion point
    insert_point = rs.GetPoint(f"Pick insertion point for {block_name}")
    if not insert_point:
        return
    
    # Import as block
    try:
        # Import the file as a block
        rs.Command(f'_-Insert _File=_Yes "{local_file}" _BlockName={block_id} _Group=_No {insert_point.X},{insert_point.Y},{insert_point.Z} 1 0 ', False)
        print(f"Successfully inserted: {block_name}")
        
    except Exception as e:
        print(f"Error inserting block: {e}")
        rs.MessageBox(f"Error inserting block: {e}", 0, "Error")


def show_library_info():
    """Display library information"""
    catalog = load_catalog()
    if not catalog:
        rs.MessageBox("Failed to load library info.", 0, "Error")
        return
    
    info = catalog.get('library_info', {})
    block_count = len(catalog.get('blocks', []))
    
    message = f"""Design Library Information:

Name: {info.get('name', 'Unknown')}
Version: {info.get('version', '1.0')}
Author: {info.get('author', 'Unknown')}
Last Updated: {info.get('updated', 'Unknown')}

Total Blocks: {block_count}
Repository: {GITHUB_USER}/{REPO_NAME}
"""
    
    rs.MessageBox(message, 0, "Library Info")


def clear_cache():
    """Clear the local cache"""
    import shutil
    try:
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
        rs.MessageBox("Cache cleared successfully!", 0, "Success")
    except Exception as e:
        rs.MessageBox(f"Error clearing cache: {e}", 0, "Error")


# ========== MAIN MENU ==========
def main():
    """Main menu for block library"""
    
    options = [
        "Browse and Insert Block",
        "Show Library Info",
        "Clear Cache",
        "Cancel"
    ]
    
    choice = rs.ListBox(options, "What would you like to do?", "Rhino Block Library")
    
    if choice == "Browse and Insert Block":
        browse_and_insert()
    elif choice == "Show Library Info":
        show_library_info()
    elif choice == "Clear Cache":
        clear_cache()


# Run the script
if __name__ == "__main__":
    main()
