import os
import frontmatter
import toml
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

def convert_obsidian_to_hugo(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, "r", encoding="utf-8") as file:
                post = frontmatter.load(file)

            # Extract metadata
            metadata = post.metadata
            title = metadata.get("title", filename.replace(".md", ""))
            date = metadata.get("Created", "2025-03-20T00:00:00+00:00")  # Default date if missing
            tags = metadata.get("tags", [])

            # Ensure tags are a list
            if isinstance(tags, str):
                tags = [tags]

            # Convert metadata to TOML
            hugo_metadata = {
                "title": title,
                "date": date,
                "tags": tags,
                "draft": True  # Default to draft mode
            }

            # Generate TOML frontmatter
            toml_frontmatter = f"+++\n{toml.dumps(hugo_metadata)}+++\n"

            # Combine TOML frontmatter with content
            new_content = toml_frontmatter + post.content

            # Write to output directory
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(new_content)

            # Print confirmation with vibrant green [+]
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {filename} => Ready to publish.")

# Usage Example
input_directory = "/home/nyx/zzz/repos/obsidian-to-hugo/obsidian_files"  # Change this to your Obsidian notes directory
output_directory = "/home/nyx/zzz/repos/obsidian-to-hugo/hugo_files"     # Where converted Hugo files will be saved
convert_obsidian_to_hugo(input_directory, output_directory)
