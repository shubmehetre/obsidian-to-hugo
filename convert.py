import os
import re
import shutil
import frontmatter
from datetime import datetime

# Required directories
OBSIDIAN_DIR = "/home/nyx/zzz/repos/obsidian-to-hugo/obsidian_files/"
MEDIA_STORAGE = "/home/nyx/zzz/synced/Palazzo/02 Misc/MediaStorage"
HUGO_STATIC = "/home/nyx/zzz/repos/main_site/static/img/"
HUGO_CONTENT = "/home/nyx/zzz/repos/main_site/content/posts/Tryhackme/"

def convert_yaml_to_toml(content, filename):
    """
    Convert YAML front matter to TOML format with proper formatting.
    """
    post = frontmatter.loads(content)
    title = post.metadata.get('title', filename.replace('.md', ''))
    created_date = post.metadata.get('Created', '')
    
    # Convert date format
    if created_date:
        dt_obj = datetime.strptime(created_date, "%d-%b-%Y %H:%M:%p")
        formatted_date = dt_obj.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    else:
        formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30")
    
    toml_frontmatter = """+++
title = '{}'
date = '{}'
showToc = true
[cover]
    image = 'cover/thm.jpg'
+++""".format(title, formatted_date)
    
    return toml_frontmatter + "\n\n" + post.content

def process_images_and_update_links(content, filename):
    """
    Find image links, copy images to Hugo's static folder, and rename them properly.
    """
    title_slug = re.sub(r'\s+', '-', filename.split('.')[0].lower())  # Convert title to slug
    img_pattern = re.findall(r'!\[\]\((Pasted%20image%20[^)]+)\)', content)
    
    img_counter = 1
    for img in img_pattern:
        orig_img_name = img.replace('%20', ' ')
        orig_img_path = os.path.join(MEDIA_STORAGE, orig_img_name)
        
        if os.path.exists(orig_img_path):
            new_img_name = f"{title_slug}-{img_counter:02d}.png"
            new_img_path = os.path.join(HUGO_STATIC, new_img_name)
            shutil.copy2(orig_img_path, new_img_path)
            content = content.replace(img, f'/img/{new_img_name}')  # Update the markdown link
            img_counter += 1
    
    return content

def convert_obsidian_to_hugo():
    """
    Process each markdown file in the Obsidian directory, convert front matter,
    copy associated images, and place converted files in Hugo content directory.
    """
    for file in os.listdir(OBSIDIAN_DIR):
        if file.endswith(".md"):
            obsidian_path = os.path.join(OBSIDIAN_DIR, file)
            hugo_path = os.path.join(HUGO_CONTENT, file)
            
            with open(obsidian_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = convert_yaml_to_toml(content, file)
            content = process_images_and_update_links(content, file)
            
            with open(hugo_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\033[92m[+] {file} => Ready to publish.\033[0m")

if __name__ == "__main__":
    convert_obsidian_to_hugo()

