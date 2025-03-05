import argparse
import urllib.parse
from collections import defaultdict

def analyze_urls(input_file, output_file=None, max_depth=None):
    domains = set()
    subdirectories = set()
    parameters = defaultdict(int)  # Dictionary to count parameter occurrences
    
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            if not url:
                continue
            
            parsed_url = urllib.parse.urlparse(url)
            domains.add(parsed_url.netloc)

            # Extract subdirectories with depth filtering
            path_parts = parsed_url.path.strip('/').split('/')
            if max_depth is None:
                subdirectories.add(parsed_url.path)  # Store full path
            else:
                filtered_path = '/' + '/'.join(path_parts[:max_depth]) if path_parts[0] else '/'
                subdirectories.add(filtered_path)

            # Extract query parameters
            query_params = urllib.parse.parse_qs(parsed_url.query)
            for param in query_params.keys():
                parameters[param] += 1

    # Prepare summary
    summary = []
    summary.append("### Unique Domains (Subdomains) ###")
    summary.extend(sorted(domains))
    
    summary.append("\n### Unique Subdirectories (Depth: {}) ###".format(max_depth if max_depth else "All"))
    summary.extend(sorted(subdirectories))
    
    summary.append("\n### Unique Parameters ###")
    for param, count in sorted(parameters.items(), key=lambda x: x[1], reverse=True):
        summary.append(f"{param} ({count} occurrences)")
    
    output_text = "\n".join(summary)

    # Print summary to console
    print(output_text)

    # Save to file if output file is specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(output_text)
        print(f"\n[+] Summary saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze URLs and extract domains, subdirectories, and parameters.")
    parser.add_argument("input_file", help="File containing a list of URLs.")
    parser.add_argument("-o", "--output", help="Optional output file to save results.")
    parser.add_argument("-d", "--depth", type=int, help="Filter subdirectories by depth (default: all levels).")

    args = parser.parse_args()
    analyze_urls(args.input_file, args.output, args.depth)
