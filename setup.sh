#!/bin/bash

# Check if the user wants to proceed with the installation
read -p "This script will install Banner and set it up for shell integration. Do you want to proceed? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Install the required packages
pip install -r requirements.txt

# Create a symbolic link for the banner.py script in /usr/local/bin
ln -s "$(pwd)/banner.py" /usr/local/bin/banner

# Check if the banners.db file exists, and if not, create it and add a default banner
if [ ! -f "banners.db" ]; then
    touch banners.db
    echo "Creating the banners.db file and adding a default banner..."
    python banner.py add "Welcome to Banner!"
fi

# Create a shell script to run the banner.py script with the random command
cat <<'EOF' > random_banner.sh
#!/bin/bash

# Run the banner.py script with the random command
banner random
EOF

chmod +x random_banner.sh

# Add the random_banner.sh script to the shell's startup file
echo 'random_banner.sh' >> ~/.bash_profile

# Inform the user about the successful installation
echo "Banner has been installed and set up for shell integration."
echo "To display a random banner, just type 'banner' in your terminal."
