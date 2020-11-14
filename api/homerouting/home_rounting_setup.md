### Server block setup
This is used to encapsulate configuration details and host more than one domain from a single server
```bash
# Create directory and set ownership/permissions
sudo mkdir -p /var/www/home.local/html
sudo chown -R ${USER}:${USER} /var/www/home.local/html
sudo chmod -R 755 /var/www/home.local
# Create sample index.html file
nano /var/www/home.local/html/index.html
```
Copy/paste this in that file 
```html
<html>
    <head>
        <title>Welcome to Home Routing!</title>
    </head>
    <body>
        <h1>Success!  The server block is working!</h1>
    </body>
</html>
```
Then let's make a new configuration file for nginx (instead of adjusting the `default`)
```bash
sudo nano /etc/nginx/sites-available/home.local
```
Copy/paste this into that file
```
server {
        listen 80;
        listen [::]:80;

        root /var/www/home.local/html;
        index index.html index.htm index.nginx-debian.html;

        server_name home.local;

        location / {
                try_files $uri $uri/ =404;
        }
}
```
Then enable the file by creating a link from it to the `sites-enabled` directory
```bash
sudo ln -s /etc/nginx/sites-available/home.local /etc/nginx/sites-enabled/
```
Correct for possible hash bucket memory problem (idk, seems like something worth avoiding)
```bash
sudo nano /etc/nginx/nginx.conf
```
Uncomment the line that has `server_names_hash_bucket_size`, save and close.
Then test nginx configs and, if succeeded, restart the service.
```bash
sudo nginx -t
sudo systemctl restart nginx
```