## Three-Server Web Infrastructure Design for www.foobar.com

#### Overview:

The infrastructure consists of three servers, each serving specific roles in ensuring availability, load balancing, and data management for hosting the website www.foobar.com.

---

### Components & Explanation

1. **Load Balancer (HAProxy)**:
    - **Role**: The load balancer will distribute incoming HTTP requests between the web servers. This ensures better resource utilization, reduces server load, and increases redundancy.
    - **Distribution Algorithm**: Round Robin or Least Connections.
        - **Round Robin**: Distributes requests evenly across servers, ensuring no single server is overwhelmed. Ideal when servers are similar in load and capability.
        - **Least Connections**: Distributes requests to the server with the fewest active connections. This is useful when traffic patterns are unpredictable and some servers may process requests faster than others.
    - **Active-Active Setup**: In this setup, both servers are active and handle traffic simultaneously. If one server fails, the other continues serving traffic. The load balancer detects the failure and reroutes traffic to the remaining healthy server.
    - **Active-Passive Setup**: Here, one server handles all the traffic (active), while the other server is on standby (passive). If the active server fails, the passive server is promoted to active. This setup is more cost-efficient but less resilient to sudden traffic spikes.

2. **Web Server (Nginx)**:
    - **Role**: Nginx will handle all static content delivery (HTML, CSS, images) and forward dynamic requests to the application server. It's optimized for high-performance static content serving and reverse proxying.
    - **Why it's needed**: Nginx can handle high numbers of concurrent connections and can act as a reverse proxy, caching static content to offload work from the application server. It can also handle SSL termination, which would be important if HTTPS is configured later.

3. **Application Server**:
    - **Role**: The application server will process the dynamic content (such as PHP, Python, or Node.js code). It interacts with the database and renders content based on user requests.
    - **Why it's needed**: The application server contains the logic and code that runs the website, enabling dynamic functionality, user interactions, and database queries.

4. **Database (MySQL)**:
    - **Role**: The database will store all dynamic content, including user data, product info, posts, and other website-related information.
    - **Primary-Replica (Master-Slave) Cluster**:
        - **Primary (Master) Node**: This node handles write operations (inserts, updates, deletes) and serves as the authoritative source of data.
        - **Replica (Slave) Node**: This node replicates data from the primary node and is used for read operations (select queries). It helps offload read traffic from the primary node, improving scalability.
    - **Why it's needed**: A distributed database setup ensures high availability (through replication) and load balancing for read queries. This setup reduces the chances of overloading the primary database node.
  
5. **Codebase (Application Files)**:
    - **Role**: These are the files that run the website, including the website's back-end logic, templates, scripts, and data processing code.
    - **Why it's needed**: Without the codebase, the web and application servers would have no logic to process user requests and serve dynamic content.

---

### Infrastructure Diagram

```
        +-------------------+
        |     HAProxy       | <--- Load Balancer (HAProxy) with Round Robin
        +-------------------+
                 |
    +------------------------+   +------------------------+
    |     Web Server 1       |   |     Web Server 2       | <--- Nginx (Reverse Proxy)
    |  (Nginx - Static Files)|   |  (Nginx - Static Files)|
    +------------------------+   +------------------------+
               |                        |
    +-----------------------+   +-----------------------+
    | Application Server 1   |   | Application Server 2   | <--- Application Logic (PHP, Node.js, etc.)
    +-----------------------+   +-----------------------+
                |
       +----------------------+
       |      MySQL Database  |
       | (Primary-Replica Setup)|
       +----------------------+
               |
         +-----------------+
         |  Replica Node   | <--- Replica of Primary DB
         +-----------------+
```

---

### Additional Explanations

#### Load Balancer (HAProxy)

- **Distribution Algorithm**: In this setup, we use the **Round Robin** distribution algorithm for simplicity. It is suitable when the web servers are similarly powered and can handle an equal number of requests. For more complex cases, **Least Connections** may be used to optimize resource utilization by sending requests to the server with the least number of current connections.
- **Active-Active vs Active-Passive**:
    - **Active-Active**: Both web servers actively handle requests. If one goes down, the load balancer automatically routes traffic to the other server. This setup provides better fault tolerance and scalability.
    - **Active-Passive**: One web server handles all requests while the other waits in standby mode. The passive server only takes over if the active one fails. This setup can be more cost-effective but doesn't scale as well under traffic spikes.

#### Database (Primary-Replica)

- **Primary Node (Master)**: This is where all the writes happen. When users submit data (like comments, orders, etc.), it goes to the primary node. It’s the authoritative source of data.
- **Replica Node (Slave)**: This node replicates the data from the primary node and serves read operations. It's used to offload read queries from the primary, enhancing performance.
- **Replication**: The replication process ensures that the replica stays synchronized with the primary node. If the primary goes down, the replica can be promoted to master.

---

### Issues with the Infrastructure

1. **Single Points of Failure (SPOF)**:
    - **Load Balancer**: If HAProxy goes down, there is no traffic distribution, which would take down the entire infrastructure. To resolve this, we could implement a secondary load balancer for failover.
    - **Database**: In a primary-replica setup, if the primary database node fails and there's no automated failover to promote the replica, the application may not function correctly. Using tools like **MySQL Router** or **Orchestrator** can help automate failover.
    - **Application Server**: If an application server fails and no redundancy is provided, that part of the infrastructure would stop handling requests.

2. **Security Issues**:
    - **No Firewall**: There is no mention of a firewall in the design. A firewall should be added to protect the servers from unauthorized access.
    - **No HTTPS**: Traffic is unencrypted by default. The use of HTTPS (SSL/TLS) should be implemented, especially for sensitive data like user logins, passwords, and payments.

3. **No Monitoring**:
    - There is no mention of any monitoring system in the design. Tools like **Prometheus**, **Grafana**, or **Datadog** should be implemented to monitor server health, traffic patterns, database performance, and load balancer stats to avoid downtimes and improve troubleshooting.
  
4. **Scalability**:
    - As the user base grows, the infrastructure will need to be scaled. For instance, more application servers or database replicas might be needed. This should be considered when designing for future growth.

---

### Summary

This three-server web infrastructure design covers the basic requirements for hosting a dynamic website with load balancing, application logic, and database management. We’ve used a load balancer for distribution, a MySQL database with replication for redundancy, and Nginx for handling web traffic. However, attention should be given to SPOFs, security, and monitoring to ensure a robust, secure, and scalable system.



## Three-Server Web Infrastructure Design for www.foobar.com (Secured, Encrypted, Monitored)

#### Overview:

This infrastructure ensures secure communication, data encryption, and ongoing monitoring, while also providing redundancy for high availability. The setup includes a web server, an application server, a database server, a load balancer, and the necessary security and monitoring components.

---

### Components & Explanation

1. **Firewalls (3)**:
    - **Role**: Firewalls are added to secure the infrastructure by controlling incoming and outgoing traffic. They are essential for blocking unauthorized access and ensuring the network is protected from potential security threats.
    - **Why Adding Firewalls**:
      - **First Firewall**: Placed at the **edge of the network**, it filters all incoming traffic from the internet before it reaches the load balancer. It ensures only safe, legitimate traffic is allowed in, blocking DDoS attacks or unauthorized access attempts.
      - **Second Firewall**: Positioned between the **load balancer** and the **web/application servers**. It ensures that only traffic from the load balancer can access these servers, limiting potential internal threats.
      - **Third Firewall**: Placed between the **application server** and the **database server**, protecting the database from unauthorized access and ensuring only the application servers can communicate with it.

2. **SSL Certificate for HTTPS**:
    - **Role**: An SSL certificate ensures that traffic between clients (users) and the web server is encrypted using HTTPS, preventing data interception and ensuring data integrity.
    - **Why Adding SSL**: 
      - **Encrypting Data**: SSL encryption ensures that all sensitive data (e.g., login credentials, payment information) is transmitted securely.
      - **Trust**: Serving traffic over HTTPS ensures users trust your website as it demonstrates commitment to data privacy.
      - **SEO Benefits**: Google and other search engines prioritize HTTPS websites, improving SEO rankings.

3. **Monitoring Clients (3)**:
    - **Role**: Monitoring tools like **SumoLogic** or **Prometheus/Grafana** are deployed to track performance, health, and usage metrics of the infrastructure. These tools help identify and resolve issues before they impact users.
    - **Why Adding Monitoring**:
      - **Real-time Monitoring**: Collects data on system health, server performance (CPU, memory usage, etc.), and web traffic metrics (requests per second, response times, error rates).
      - **Alerting**: Configures alerts to notify administrators of issues like server failure, high latency, or high error rates.
      - **Traffic Analysis**: Monitors usage patterns, helping with scalability planning.
    - **How Monitoring Tool Collects Data**: Monitoring clients are installed on each server (web, application, database), where they collect system and application logs, performance metrics (e.g., CPU load, disk I/O, QPS), and errors. These are sent to a centralized monitoring system (e.g., Sumologic, Prometheus, or Datadog) for analysis and reporting.

4. **Load Balancer (HAProxy)**:
    - **Role**: The load balancer distributes incoming web traffic across multiple web servers (if available), ensuring no server is overwhelmed and improving availability.
    - **Why Adding Load Balancer**: It provides horizontal scalability and ensures high availability by rerouting traffic in case of server failure.
    - **HTTPS Termination**: SSL/TLS certificates are terminated at the load balancer level (encrypted traffic decrypted here before being forwarded to the application or web servers), ensuring secure communication between the client and the infrastructure.

5. **Web Servers (Nginx)**:
    - **Role**: These servers handle HTTP requests, serve static content (HTML, CSS, JavaScript), and pass dynamic requests to the application server.
    - **Why Adding Web Servers**: They offload static content delivery from the application server, which improves performance and scalability. Nginx also handles SSL termination in this architecture.
   
6. **Application Servers**:
    - **Role**: The application server runs the business logic, communicates with the database, and serves dynamic content (e.g., user authentication, transactions).
    - **Why Adding Application Servers**: These servers handle the dynamic, data-driven parts of the website (e.g., processing user input, making API calls). By separating the application logic from the web server, the infrastructure can scale more easily.

7. **Database (MySQL with Replication)**:
    - **Role**: MySQL stores all dynamic content and data (user accounts, products, etc.). A replication setup with one primary node (master) and one replica (slave) is used to scale read queries.
    - **Why Adding MySQL**: A relational database like MySQL is needed to manage user and application data. MySQL replication allows for a highly available database system and read scalability.

---

### Infrastructure Diagram

```
                   +---------------------+
                   |     Firewall 1       | <--- Edge Firewall (blocks malicious external traffic)
                   +---------------------+
                            |
                   +---------------------+
                   |     Load Balancer    | <--- HAProxy (handles SSL termination and load balancing)
                   +---------------------+
                            |
                +-----------+-----------+  
                |                       |
      +------------------+       +------------------+
      |   Web Server 1   |       |   Web Server 2   | <--- Nginx (serves static content, handles SSL)
      +------------------+       +------------------+
                |                       |
         +----------------+       +----------------+
         | Application 1  |       | Application 2  | <--- Application Logic (PHP, Node.js, etc.)
         +----------------+       +----------------+
                |                       |
        +----------------+         +----------------+
        |   MySQL Master |         |    MySQL Replica| <--- Primary-Replica DB Setup
        +----------------+         +----------------+
```

---

### Additional Explanations

#### 1. **Why Add Firewalls?**
   - **Edge Security**: Firewalls prevent unauthorized access by controlling incoming and outgoing network traffic.
   - **Internal Segmentation**: Placing firewalls between components (load balancer, web servers, database) ensures that only specific services can talk to each other, preventing unnecessary exposure to potential attacks.

#### 2. **Why Serve Traffic Over HTTPS?**
   - **Data Encryption**: SSL/TLS encrypts traffic, preventing third parties from intercepting sensitive data.
   - **Authentication**: SSL certificates also authenticate the website, ensuring users communicate with the legitimate site.
   - **User Trust**: HTTPS ensures that users’ personal information is securely transmitted.
   - **SEO Advantage**: Google prioritizes HTTPS websites over HTTP in search rankings.

#### 3. **What is Monitoring Used For?**
   - **System Performance**: Monitors server health, resources (CPU, memory, disk), and uptime.
   - **Application Metrics**: Monitors web traffic, error rates, and application performance (such as QPS).
   - **Alerting**: Provides real-time alerts when thresholds are breached (e.g., high error rates, low server availability).
   - **Scalability**: Helps plan for resource scaling based on usage patterns.

#### 4. **How Monitoring Collects Data:**
   - **Metrics Collection**: Monitoring agents are installed on each server (application, web, and database) to collect performance and log data.
   - **Centralized Analysis**: Collected data is sent to a central system like **Sumologic**, **Prometheus**, or **Datadog** for aggregation and analysis.
   - **Web Server QPS Monitoring**: To monitor Queries Per Second (QPS), configure the monitoring system to track the number of requests per second hitting the web server. This data can be visualized via a dashboard like **Grafana**, or alerts can be set if QPS exceeds certain thresholds.

---

### Issues with the Infrastructure

1. **Terminating SSL at the Load Balancer Level**:
    - **Issue**: Terminating SSL at the load balancer can potentially expose decrypted traffic between the load balancer and the backend web/application servers, unless that traffic is encrypted internally (e.g., via internal TLS). 
    - **Potential Solution**: Use end-to-end encryption (TLS) from client to backend servers, or ensure internal network communication is encrypted.

2. **Single Writeable MySQL Server (Master)**:
    - **Issue**: Having only one writeable MySQL server (master) creates a **single point of failure** for write operations. If the master goes down, the system cannot accept any new data until the master is restored or a new master is promoted.
    - **Potential Solution**: Implement **automated failover** using **MySQL Group Replication** or **Orchestrator** to ensure that if the master fails, the replica is automatically promoted to master.

3. **Same Components on All Servers (Web, Application, Database)**:
    - **Issue**: Hosting web, application, and database components on the same server increases complexity and resource contention. These servers might not scale effectively under heavy traffic or demand.
    - **Potential Solution**: Separate components into dedicated servers or containers (e.g., using **Docker** and **Kubernetes**), which allows the infrastructure to scale independently based on the needs of each service.

---

### Summary

This three-server infrastructure provides a **secure**, **scalable**, and **monitored** environment for hosting the website www.foobar.com. By adding firewalls, SSL certificates, and monitoring clients, the system ensures that user data is protected, performance is continuously tracked, and potential issues are flagged early. However, there are some challenges like potential SSL exposure, database write limitations, and resource contention that should be addressed to ensure optimal performance and availability.



## Multi-Server Web Infrastructure Design with Load Balancer Cluster

#### Overview:
In this design, we will split the components (web server, application server, and database server) onto separate servers and add a **load balancer cluster** for enhanced redundancy and traffic distribution. This approach allows for better scalability, high availability, and fault tolerance.

---

### Infrastructure Components

1. **Two Load Balancers (HAProxy Cluster)**:
    - **Role**: The load balancers distribute incoming HTTP traffic to multiple web servers (if available). By configuring them in a cluster, we achieve fault tolerance and avoid a **single point of failure** for traffic distribution.
    - **Why Add Load Balancer Cluster**:
        - **High Availability**: If one load balancer fails, the other one can take over the traffic, ensuring continuous availability.
        - **Traffic Distribution**: Distributes client requests to web servers based on a set algorithm (e.g., Round Robin, Least Connections, or IP Hash). This ensures that no single server is overwhelmed.
        - **Redundancy**: In the case of a failure in one load balancer, the other will keep distributing traffic, maintaining uptime and performance.

2. **Web Server (Nginx)**:
    - **Role**: The web server will serve static content like HTML, CSS, JavaScript, and images. It can also handle SSL termination, caching, and reverse proxying to the application server for dynamic content.
    - **Why Add Web Server**:
        - **Separation of Static and Dynamic Content**: By using Nginx as a web server, we can offload static content from the application server, allowing it to focus on business logic.
        - **SSL Termination**: Nginx can handle SSL decryption (if HTTPS is configured), which offloads the SSL burden from the application server, improving performance.
        - **Load Balancer Integration**: Nginx works in conjunction with the load balancer, receiving traffic that has been distributed, and can handle the front-end requests efficiently.

3. **Application Server (PHP, Node.js, Python, etc.)**:
    - **Role**: The application server will run the business logic of the website, handling dynamic content (such as processing form submissions, managing sessions, and making database queries).
    - **Why Add Application Server**:
        - **Separation of Concerns**: Keeping the application logic separate from the web server (which serves static content) improves scalability, maintainability, and load balancing.
        - **Dynamic Content Processing**: The application server handles the server-side logic, communicating with the database, generating dynamic content, and sending it back to the web server for delivery.
        - **Scalability**: By isolating the application layer, it becomes easier to scale the application servers independently based on demand.

4. **Database Server (MySQL)**:
    - **Role**: The database server stores all dynamic data, including user information, posts, transactions, etc. This server is essential for data persistence and is used by the application server for storing and retrieving data.
    - **Why Add Database Server**:
        - **Data Storage**: The database server handles read and write requests from the application server, storing and retrieving data as needed.
        - **Separation of Database Layer**: By separating the database from the application and web servers, we avoid resource contention and ensure the database can be optimized for performance and scalability.
        - **Scalability**: The database server can be configured for replication or clustering to ensure availability and scaling of read/write operations.

---

### Infrastructure Diagram

```
                        +---------------------+
                        |    Load Balancer    | <--- HAProxy Cluster (distributes traffic)
                        |      (HAProxy)      |
                        +---------------------+
                              /        \
                +-----------------+    +-----------------+
                |   Web Server 1  |    |   Web Server 2  | <--- Nginx (static content, reverse proxy)
                +-----------------+    +-----------------+
                        |                     |
              +-------------------+    +-------------------+
              | Application Server |    | Application Server | <--- (PHP, Node.js, etc.)
              +-------------------+    +-------------------+
                        |
                +-----------------+
                |   Database      | <--- MySQL Database (stores dynamic data)
                |    Server       |
                +-----------------+
```

---

### Specifics and Explanations

#### 1. **Load Balancer Cluster (HAProxy)**

- **Why Add It**: The load balancer cluster consists of two HAProxy instances that work together to distribute incoming traffic. In this setup:
  - **High Availability**: If one load balancer fails, the other takes over, ensuring no disruption in service.
  - **Load Distribution**: It ensures that no individual server gets overwhelmed by too many requests. HAProxy uses algorithms like **Round Robin**, **Least Connections**, or **IP Hash** to intelligently route traffic based on the number of requests or active connections.
  
- **How It Works**: HAProxy acts as a reverse proxy, sitting in front of the web servers and receiving all HTTP requests from users. The load balancer decides which server (among Web Server 1, Web Server 2) should handle the request based on the chosen load balancing strategy.

#### 2. **Web Server (Nginx)**

- **Why Add It**: The web server handles static content and forwards dynamic requests to the application server. It acts as a reverse proxy between the client and the backend servers.
  - **SSL Termination**: If HTTPS is configured, Nginx can handle SSL decryption, offloading this task from the application servers.
  - **Caching and Load Balancing**: Nginx can cache static content, improving performance, and it can also distribute requests between multiple application servers if needed.
  
- **How It Works**: The web server serves static files (images, CSS, JavaScript) directly. For dynamic requests (e.g., user authentication, database queries), it forwards these requests to the application server via HTTP or another internal protocol.

#### 3. **Application Server**

- **Why Add It**: The application server is responsible for handling dynamic content, such as running the backend code, interacting with databases, and managing user sessions. It processes the data coming from the user, performs business logic, and generates the dynamic content returned to the client.
  - **Scalability**: If more application servers are needed (due to traffic spikes or load), additional application servers can be added without disrupting the web or database layers.
  - **Separation of Logic**: By isolating the application logic, we reduce the workload on the web server and focus each layer on its core responsibilities.
  
- **How It Works**: The application server runs the application logic (e.g., PHP, Node.js, or Python), processes incoming requests, interacts with the database server, and returns dynamic content to the web server, which then sends it to the client.

#### 4. **Database Server (MySQL)**

- **Why Add It**: The database server stores all user and application data, such as user accounts, transactions, or other dynamic content. A dedicated database server ensures that data is stored reliably and can scale to handle large datasets.
  - **Data Integrity**: A separate database server improves data management, backup, and security. It is easier to optimize this layer for performance without interfering with the application or web server layers.
  - **Scalability**: The database can be configured with **replication** (Primary-Replica) to increase read performance by distributing read queries across multiple nodes.
  
- **How It Works**: The application server communicates with the database server to store and retrieve data. The database server performs these read/write operations while ensuring data consistency and integrity.

---

### Key Considerations and Potential Issues

1. **Load Balancer Cluster Configuration**:
   - **Issue**: If the load balancer cluster is not set up with proper failover mechanisms, a failure in one load balancer could cause downtime. 
   - **Solution**: Ensure that the load balancer cluster uses active-active configuration or failover mechanisms to maintain high availability.

2. **Web Server and Application Server Separation**:
   - **Issue**: There could be inefficiencies if both the web and application servers are placed on the same machine. The web server could potentially overload the application server with traffic, limiting performance.
   - **Solution**: By separating these components across different servers, you allow each layer to scale independently based on its own workload.

3. **Database Server Bottleneck**:
   - **Issue**: If the database server is a single point of failure, and it cannot handle the combined read and write loads, the system performance may degrade.
   - **Solution**: Use **replication** (Primary-Replica) or **clustering** (such as Galera Cluster for MySQL) to distribute read operations and ensure high availability for write operations.

---

### Summary

In this infrastructure design, we have separated the different components (web server, application server, and database server) across multiple servers to ensure **scalability**, **fault tolerance**, and **high availability**. The **HAProxy load balancer cluster** ensures that traffic is evenly distributed across the web servers, providing fault tolerance. The **SSL certificate** secures traffic between clients and servers. By splitting components across separate servers, the infrastructure is better optimized for handling larger traffic loads, ensuring long-term scalability, and allowing each component to be independently scaled or maintained.


