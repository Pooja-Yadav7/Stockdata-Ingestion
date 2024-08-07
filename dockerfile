FROM mysql:8.0

# Set environment variables for MySQL
ENV MYSQL_DATABASE=stock_data
ENV MYSQL_ROOT_PASSWORD=Stock@12345


# Expose the MySQL port
EXPOSE 3306
