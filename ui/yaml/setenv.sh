# Environment variables 
apiBack=$API_URL
echo "Generating env.js file"
echo -e "(function (window) {\n  
window.__env = window.__env || {};\n
// APIs urls we set this by environment   \n
window.__env.apiUrl = '$apiBack';\n
}(this));" > /usr/share/nginx/html/env.js
