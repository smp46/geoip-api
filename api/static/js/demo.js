document.addEventListener('DOMContentLoaded', function() {
    const ipInput = document.getElementById('ip-input');
    const lookupBtn = document.getElementById('lookup-btn');
    const resultContainer = document.getElementById('result-container');
    const resultElement = document.getElementById('result');
    const copyResultBtn = document.getElementById('copy-result');
    const resultFlagContainer = document.getElementById('result-flag-container');
    
    // Example IP addresses for placeholder rotation
    const exampleIPs = [
        '8.8.8.8',         // Google DNS (US)
        '1.1.1.1',         // Cloudflare (AU)
        '208.67.222.222',  // OpenDNS (US)
        '185.228.168.168', // CleanBrowsing (NO)
        '9.9.9.9',         // Quad9 (US)
        '64.6.64.6'        // Verisign (US)
    ];
    
    // Function to highlight JSON syntax
    function formatJSON(json) {
        if (typeof json !== 'string') {
            json = JSON.stringify(json, null, 2);
        }
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, 
            function (match) {
                let cls = 'number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                    } else {
                        cls = 'string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'boolean';
                } else if (/null/.test(match)) {
                    cls = 'null';
                }
                return '<span class="' + cls + '">' + match + '</span>';
            }
        );
    }
    
    // Function to display animated flag
    function displayFlag(countryCode) {
        if (!countryCode) return;
        
        // Clear previous flag
        resultFlagContainer.innerHTML = '';
        
        // Create flag element
        const flagPlayer = document.createElement('tgs-player');
        flagPlayer.setAttribute('src', `https://Malith-Rukshan.github.io/animated-country-flags/tgs/${countryCode}.tgs`);
        flagPlayer.setAttribute('autoplay', '');
        flagPlayer.setAttribute('loop', '');
        flagPlayer.style.width = '150px';
        flagPlayer.style.height = '150px';
        
        // Add flag to container
        resultFlagContainer.appendChild(flagPlayer);
        resultFlagContainer.style.display = 'flex';
    }
    
    // Function to perform IP lookup
    async function lookupIP(ip) {
        try {
            // Show loading state
            resultElement.innerHTML = 'Loading...';
            resultContainer.style.display = 'block';
            resultFlagContainer.style.display = 'none';
            
            // Make API request
            const response = await fetch(`/api/v1/geoip/lookup/${ip}`);
            const data = await response.json();
            
            // Display formatted result
            resultElement.innerHTML = formatJSON(data);
            
            // Display flag if country code is available
            if (data.code) {
                displayFlag(data.code);
            }
            
        } catch (error) {
            resultElement.innerHTML = `Error: ${error.message}`;
            resultFlagContainer.style.display = 'none';
        }
    }
    
    // Set up button click handler
    lookupBtn.addEventListener('click', function() {
        const ip = ipInput.value.trim();
        if (ip) {
            lookupIP(ip);
        } else {
            alert('Please enter an IP address');
        }
    });
    
    // Set up enter key handler
    ipInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const ip = ipInput.value.trim();
            if (ip) {
                lookupIP(ip);
            }
        }
    });
    
    // Copy result to clipboard
    copyResultBtn.addEventListener('click', function() {
        const textToCopy = resultElement.textContent;
        
        navigator.clipboard.writeText(textToCopy).then(function() {
            // Temporarily change the button icon to indicate success
            copyResultBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(function() {
                copyResultBtn.innerHTML = '<i class="far fa-copy"></i>';
            }, 1500);
        }).catch(function(err) {
            console.error('Could not copy text: ', err);
        });
    });
    
    // Copy endpoint examples
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Temporarily change the button icon to indicate success
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="far fa-copy"></i>';
                }, 1500);
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
        });
    });
    
    // Rotate placeholder examples
    let placeholderIndex = 0;
    
    function rotatePlaceholder() {
        ipInput.setAttribute('placeholder', `Enter an IP address (e.g., ${exampleIPs[placeholderIndex]})`);
        placeholderIndex = (placeholderIndex + 1) % exampleIPs.length;
    }
    
    // Initial placeholder
    rotatePlaceholder();
    
    // Rotate placeholder every 3 seconds
    setInterval(rotatePlaceholder, 3000);

    // Add animation to the globe
    window.onload = function() {
        const globe = document.getElementById('globe-animation');
        // Add animation code here, or use an image/SVG as a placeholder
        globe.innerHTML = `
            <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
                <circle cx="200" cy="200" r="180" fill="#3a0ca3" opacity="0.1"/>
                <circle cx="200" cy="200" r="150" fill="none" stroke="#4361ee" stroke-width="2" stroke-dasharray="5,5"/>
                <circle cx="200" cy="200" r="120" fill="none" stroke="#4361ee" stroke-width="2"/>
                <path d="M200,80 C270,80 340,150 340,200 C340,270 270,320 200,320 C130,320 60,270 60,200 C60,150 130,80 200,80 Z" fill="none" stroke="#f72585" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="#4361ee" opacity="0.2"/>
            </svg>
        `;
    };
});