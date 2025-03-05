import os
import subprocess

# Function to check if the subdomain is active using curl
def check_subdomain(subdomain, base_url):
    # Convert the subdomain to lowercase
    subdomain = subdomain.lower()

    # Full URL to check
    url = f"https://{subdomain}.{base_url}"

    # Print the current subdomain being checked for debugging
    print(f"Checking: {url}")

    # Run the curl command with -sk to avoid certificate validation and output status code
    try:
        result = subprocess.run(
            ['curl', '-sk', '-o', '/dev/null', '-w', '%{http_code}', url, '--max-time', '10'],
            capture_output=True, text=True
        )

        # Capture the HTTP response code
        status_code = result.stdout.strip()
        print(f"Response code for {url}: {status_code}")  # Debugging output

        # If status code is 200, the subdomain is active
        if status_code == "200":
            print(f"Active: {url}")
            return url
        elif status_code == "301" or status_code == "302":
            # Handle redirects if needed (301, 302 codes)
            print(f"Redirected: {url}")
        else:
            print(f"Not Active: {url} - HTTP Code: {status_code}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking {url}: {e}")
    except Exception as e:
        print(f"Unexpected error checking {url}: {e}")
    return None

# Read the user-provided wordlist file and check each subdomain
def find_active_subdomains(wordlist_file, base_url, output_file):
    # Check if the wordlist file exists
    if not os.path.exists(wordlist_file):
        print(f"Error: {wordlist_file} cannot be found.")
        return

    # Open the output file to store results
    with open(output_file, 'w') as output:
        # Open and read the wordlist.txt file
        with open(wordlist_file, 'r') as wordlist:
            for line in wordlist:
                subdomain = line.strip()
                if subdomain:
                    # Check the subdomain and write it to the output file if it's active
                    active_url = check_subdomain(subdomain, base_url)
                    if active_url:
                        output.write(active_url + '\n')  # Write to results.txt
                    else:
                        print(f"{subdomain} is not active.")
                else:
                    print("Skipping empty line or invalid subdomain.")

    print(f"Subdomain scanning completed. Results saved to {output_file}.")

# Main function to handle user input
def main():
    # Ask user for the wordlist file path
    wordlist_file = input("Enter the path to your wordlist file: ")

    # Ask user for the base URL (target domain)
    base_url = input("Enter the target domain (e.g., example.com): ")

    # Ensure the user includes the domain (no 'http' or 'https' prefix)
    if base_url.startswith("http://"):
        base_url = base_url[len("http://"):]
    elif base_url.startswith("https://"):
        base_url = base_url[len("https://"):]

    # Ask user for the output file name (default is 'results.txt')
    output_file = input("Enter the output file name (default: results.txt): ")

    # If the user does not provide an output file name, use 'results.txt'
    if not output_file:
        output_file = 'results.txt'

    # Call the function to find active subdomains
    find_active_subdomains(wordlist_file, base_url, output_file)

if __name__ == '__main__':
    main()













































8
