CREATE TABLE visit_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    page_name VARCHAR(255),
    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE missing_data_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requested_item VARCHAR(255),
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    missing_reason TEXT
);
