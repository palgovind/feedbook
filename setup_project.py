# setup_project.py
import os

project_structure = {
    "pom.xml": '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.5</version>
        <relativePath/>
    </parent>
    <groupId>com.example</groupId>
    <artifactId>feedbook</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>feedbook</name>
    <description>RBAC 3D CAD Visualization Platform</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>
        <dependency>
            <groupId>org.thymeleaf.extras</groupId>
            <artifactId>thymeleaf-extras-springsecurity6</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>''',

    "src/main/resources/application.properties": '''spring.application.name=feedbook
spring.datasource.url=jdbc:postgresql://localhost:5432/cad_db
spring.datasource.username=your_postgres_user
spring.datasource.password=your_postgres_password
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=update

autodesk.aps.client-id=YOUR_APS_CLIENT_ID
autodesk.aps.client-secret=YOUR_APS_CLIENT_SECRET''',

    "src/main/resources/schema.sql": '''CREATE TABLE IF NOT EXISTS drawings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    aps_urn VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drawing_comments (
    id SERIAL PRIMARY KEY,
    drawing_id INT REFERENCES drawings(id) ON DELETE CASCADE,
    username VARCHAR(100) NOT NULL,
    comment_text TEXT NOT NULL,
    camera_state TEXT NOT NULL,
    db_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);''',

    "src/main/java/com/example/cadplatform/FeedbookApplication.java": '''package com.example.cadplatform;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class FeedbookApplication {
    public static void main(String[] args) {
        SpringApplication.run(FeedbookApplication.class, args);
    }
}''',

    "src/main/java/com/example/cadplatform/config/SecurityConfig.java": '''package com.example.cadplatform.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.ignoringRequestMatchers("/api/**"))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
                .requestMatchers(HttpMethod.POST, "/drawings/upload").hasRole("DRAFTER")
                .requestMatchers(HttpMethod.DELETE, "/drawings/**").hasRole("DRAFTER")
                .requestMatchers("/drawings/{id}").hasAnyRole("CLIENT", "DRAFTER")
                .requestMatchers(HttpMethod.POST, "/api/comments").hasAnyRole("CLIENT", "DRAFTER")
                .requestMatchers(HttpMethod.GET, "/api/comments/drawing/**").hasAnyRole("CLIENT", "DRAFTER")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .defaultSuccessUrl("/dashboard", true)
                .permitAll()
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login?logout")
                .permitAll()
            );

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}''',

    "src/main/java/com/example/cadplatform/model/Drawing.java": '''package com.example.cadplatform.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "drawings")
public class Drawing {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false)
    private String title;
    @Column(name = "aps_urn", nullable = false, length = 500)
    private String apsUrn;
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() { this.createdAt = LocalDateTime.now(); }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getApsUrn() { return apsUrn; }
    public void setApsUrn(String apsUrn) { this.apsUrn = apsUrn; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}''',

    "src/main/java/com/example/cadplatform/model/Role.java": '''package com.example.cadplatform.model;

import jakarta.persistence.*;

@Entity
@Table(name = "roles")
public class Role {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(unique = true, nullable = false)
    private String name;

    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}''',

    "src/main/java/com/example/cadplatform/model/User.java": '''package com.example.cadplatform.model;

import jakarta.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(unique = true, nullable = false)
    private String username;
    @Column(nullable = false)
    private String password;
    private boolean enabled = true;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
        name = "users_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<Role> roles = new HashSet<>();

    public Long getId() { return id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public Set<Role> getRoles() { return roles; }
    public void setRoles(Set<Role> roles) { this.roles = roles; }
}''',

    "src/main/java/com/example/cadplatform/model/DrawingComment.java": '''package com.example.cadplatform.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "drawing_comments")
public class DrawingComment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "drawing_id", nullable = false)
    private Long drawingId;
    @Column(nullable = false)
    private String username;
    @Column(name = "comment_text", nullable = false, columnDefinition = "TEXT")
    private String commentText;
    @Column(name = "camera_state", nullable = false, columnDefinition = "TEXT")
    private String cameraState;
    @Column(name = "db_id")
    private Integer dbId;
    private LocalDateTime createdAt = LocalDateTime.now();

    public Long getId() { return id; }
    public Long getDrawingId() { return drawingId; }
    public void setDrawingId(Long drawingId) { this.drawingId = drawingId; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getCommentText() { return commentText; }
    public void setCommentText(String commentText) { this.commentText = commentText; }
    public String getCameraState() { return cameraState; }
    public void setCameraState(String cameraState) { this.cameraState = cameraState; }
    public Integer getDbId() { return dbId; }
    public void setDbId(Integer dbId) { this.dbId = dbId; }
}''',

    "src/main/java/com/example/cadplatform/dto/CommentRequest.java": '''package com.example.cadplatform.dto;

public class CommentRequest {
    private Long drawingId;
    private String commentText;
    private String cameraState;
    private Integer dbId;

    public Long getDrawingId() { return drawingId; }
    public void setDrawingId(Long drawingId) { this.drawingId = drawingId; }
    public String getCommentText() { return commentText; }
    public void setCommentText(String commentText) { this.commentText = commentText; }
    public String getCameraState() { return cameraState; }
    public void setCameraState(String cameraState) { this.cameraState = cameraState; }
    public Integer getDbId() { return dbId; }
    public void setDbId(Integer dbId) { this.dbId = dbId; }
}''',

    "src/main/java/com/example/cadplatform/dto/ApsTokenResponse.java": '''package com.example.cadplatform.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ApsTokenResponse {
    @JsonProperty("access_token") private String accessToken;
    @JsonProperty("token_type") private String tokenType;
    @JsonProperty("expires_in") private long expiresIn;

    public String getAccessToken() { return accessToken; }
    public long getExpiresIn() { return expiresIn; }
}''',

    "src/main/java/com/example/cadplatform/repository/DrawingRepository.java": '''package com.example.cadplatform.repository;

import com.example.cadplatform.model.Drawing;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface DrawingRepository extends JpaRepository<Drawing, Long> {
    List<Drawing> findAllByOrderByCreatedAtDesc();
}''',

    "src/main/java/com/example/cadplatform/repository/UserRepository.java": '''package com.example.cadplatform.repository;

import com.example.cadplatform.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}''',

    "src/main/java/com/example/cadplatform/repository/CommentRepository.java": '''package com.example.cadplatform.repository;

import com.example.cadplatform.model.DrawingComment;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface CommentRepository extends JpaRepository<DrawingComment, Long> {
    List<DrawingComment> findByDrawingIdOrderByCreatedAtDesc(Long drawingId);
}''',

    "src/main/java/com/example/cadplatform/service/CustomUserDetailsService.java": '''package com.example.cadplatform.service;

import com.example.cadplatform.model.User;
import com.example.cadplatform.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.Service;
import java.util.stream.Collectors;

@Service
public class CustomUserDetailsService implements UserDetailsService {
    @Autowired private UserRepository userRepository;
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        return new org.springframework.security.core.userdetails.User(
                user.getUsername(), user.getPassword(),
                user.getRoles().stream().map(r -> new SimpleGrantedAuthority(r.getName())).collect(Collectors.toList())
        );
    }
}''',

    "src/main/java/com/example/cadplatform/service/AutodeskAuthService.java": '''package com.example.cadplatform.service;

import com.example.cadplatform.dto.ApsTokenResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import java.time.Instant;

@Service
public class AutodeskAuthService {
    @Value("${autodesk.aps.client-id}") private String clientId;
    @Value("${autodesk.aps.client-secret}") private String clientSecret;
    private final WebClient webClient = WebClient.builder().baseUrl("https://developer.api.autodesk.com").build();

    private String cachedInternalToken;
    private Instant internalTokenExpiry = Instant.MIN;
    private String cachedPublicToken;
    private Instant publicTokenExpiry = Instant.MIN;

    public synchronized String getInternalWriteToken() {
        if (Instant.now().isBefore(internalTokenExpiry)) return cachedInternalToken;
        ApsTokenResponse res = fetchToken("bucket:create bucket:read bucket:write data:write data:read");
        cachedInternalToken = res.getAccessToken();
        internalTokenExpiry = Instant.now().plusSeconds(res.getExpiresIn() - 60);
        return cachedInternalToken;
    }

    public synchronized String getPublicViewToken() {
        if (Instant.now().isBefore(publicTokenExpiry)) return cachedPublicToken;
        ApsTokenResponse res = fetchToken("viewables:read");
        cachedPublicToken = res.getAccessToken();
        publicTokenExpiry = Instant.now().plusSeconds(res.getExpiresIn() - 60);
        return cachedPublicToken;
    }

    private ApsTokenResponse fetchToken(String scopes) {
        MultiValueMap<String, String> formData = new LinkedMultiValueMap<>();
        formData.add("client_id", clientId);
        formData.add("client_secret", clientSecret);
        formData.add("grant_type", "client_credentials");
        formData.add("scope", scopes);

        return webClient.post()
                .uri("/authentication/v2/token")
                .header("Content-Type", "application/x-www-form-urlencoded")
                .body(BodyInserters.fromFormData(formData))
                .retrieve()
                .bodyToMono(ApsTokenResponse.class)
                .block();
    }
}''',

    "src/main/java/com/example/cadplatform/service/CadUploadService.java": '''package com.example.cadplatform.service;

import com.example.cadplatform.model.Drawing;
import com.example.cadplatform.repository.DrawingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import java.io.IOException;
import java.util.Base64;
import java.util.Map;

@Service
public class CadUploadService {
    @Autowired private DrawingRepository drawingRepository;
    private final WebClient webClient = WebClient.builder().baseUrl("https://developer.api.autodesk.com").build();

    public Drawing processCadUpload(String title, MultipartFile file, String token) throws IOException {
        String objectKey = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        Map uploadResponse = webClient.put()
                .uri("/oss/v2/buckets/your_aps_bucket_key/objects/" + objectKey)
                .header("Authorization", "Bearer " + token)
                .header("Content-Type", "application/octet-stream")
                .bodyValue(file.getBytes())
                .retrieve().bodyToMono(Map.class).block();

        String rawUrn = (String) uploadResponse.get("urn");
        String base64Urn = Base64.getUrlEncoder().encodeToString(rawUrn.getBytes()).replace("=", "");

        String jsonPayload = "{\"input\": {\"urn\": \"" + base64Urn + "\" }, \"output\": {\"formats\": [{\"type\": \"svf2\", \"views\": [\"2d\", \"3d\"]}]}}";
        webClient.post().uri("/modelderivative/v2/designdata/job")
                .header("Authorization", "Bearer " + token)
                .header("Content-Type", "application/json")
                .bodyValue(jsonPayload).retrieve().toBodilessEntity().block();

        Drawing drawing = new Drawing();
        drawing.setTitle(title);
        drawing.setApsUrn(base64Urn);
        return drawingRepository.save(drawing);
    }
}''',

    "src/main/java/com/example/cadplatform/controller/DashboardController.java": '''package com.example.cadplatform.controller;

import com.example.cadplatform.repository.DrawingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {
    @Autowired private DrawingRepository drawingRepository;
    @GetMapping("/dashboard")
    public String showDashboard(Model model) {
        model.addAttribute("username", SecurityContextHolder.getContext().getAuthentication().getName());
        model.addAttribute("drawings", drawingRepository.findAllByOrderByCreatedAtDesc());
        return "dashboard";
    }
}''',

    "src/main/java/com/example/cadplatform/controller/DrawingController.java": '''package com.example.cadplatform.controller;

import com.example.cadplatform.model.Drawing;
import com.example.cadplatform.repository.DrawingRepository;
import com.example.cadplatform.service.AutodeskAuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class DrawingController {
    @Autowired private DrawingRepository drawingRepository;
    @Autowired private AutodeskAuthService autodeskAuthService;

    @GetMapping("/drawings/{id}")
    public String viewDrawing(@PathVariable Long id, Model model) {
        Drawing drawing = drawingRepository.findById(id).orElseThrow();
        model.addAttribute("drawingId", drawing.getId());
        model.addAttribute("urn", drawing.getApsUrn());
        model.addAttribute("accessToken", autodeskAuthService.getPublicViewToken());
        model.addAttribute("userRole", SecurityContextHolder.getContext().getAuthentication().getAuthorities().toString());
        return "viewer";
    }
}''',

    "src/main/java/com/example/cadplatform/controller/DrawingUploadController.java": '''package com.example.cadplatform.controller;

import com.example.cadplatform.service.AutodeskAuthService;
import com.example.cadplatform.service.CadUploadService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class DrawingUploadController {
    @Autowired private CadUploadService cadUploadService;
    @Autowired private AutodeskAuthService autodeskAuthService;

    @PreAuthorize("hasRole('DRAFTER')")
    @PostMapping("/drawings/upload")
    public String uploadDrawing(@RequestParam String title, @RequestParam MultipartFile cadFile) {
        try {
            cadUploadService.processCadUpload(title, cadFile, autodeskAuthService.getInternalWriteToken());
        } catch (Exception e) { e.printStackTrace(); }
        return "redirect:/dashboard";
    }
}''',

    "src/main/java/com/example/cadplatform/controller/CommentRestController.java": '''package com.example.cadplatform.controller;

import com.example.cadplatform.dto.CommentRequest;
import com.example.cadplatform.model.DrawingComment;
import com.example.cadplatform.repository.CommentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/comments")
public class CommentRestController {
    @Autowired private CommentRepository commentRepository;

    @PostMapping
    public ResponseEntity<DrawingComment> createComment(@RequestBody CommentRequest req) {
        DrawingComment comment = new DrawingComment();
        comment.setDrawingId(req.getDrawingId());
        comment.setUsername(SecurityContextHolder.getContext().getAuthentication().getName());
        comment.setCommentText(req.getCommentText());
        comment.setCameraState(req.getCameraState());
        comment.setDbId(req.getDbId());
        return ResponseEntity.ok(commentRepository.save(comment));
    }

    @GetMapping("/drawing/{drawingId}")
    public ResponseEntity<List<DrawingComment>> getComments(@PathVariable Long drawingId) {
        return ResponseEntity.ok(commentRepository.findByDrawingIdOrderByCreatedAtDesc(drawingId));
    }
}''',

    "src/main/resources/templates/dashboard.html": '''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" xmlns:sec="http://www.thymeleaf.org/extras/spring-security">
<head>
    <title>Nexus CAD Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark px-4">
        <a class="navbar-brand" href="#">⚙️ NEXUS CAD PORTAL</a>
        <span class="text-white">User: <strong th:text="${username}"></strong></span>
    </nav>
    <div class="container my-5">
        <div sec:authorize="hasRole('DRAFTER')" class="card p-4 mb-4 shadow-sm">
            <h5>Publish New CAD Asset</h5>
            <form action="/drawings/upload" method="POST" enctype="multipart/form-data">
                <input type="text" name="title" class="form-control mb-2" placeholder="Project Name" required>
                <input type="file" name="cadFile" class="form-control mb-2" accept=".dwg,.rvt" required>
                <button type="submit" class="btn btn-primary">Upload & Compile</button>
            </form>
        </div>
        <h4>Blueprints</h4>
        <div class="row">
            <div class="col-md-4" th:each="d : ${drawings}">
                <div class="card p-3 mb-3 shadow-sm">
                    <h5 th:text="${d.title}"></h5>
                    <a th:href="@{/drawings/{id}(id=${d.id})}" class="btn btn-outline-dark mt-2">Launch Viewer</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>''',

    "src/main/resources/templates/viewer.html": '''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>3D CAD Workspace</title>
    <link rel="stylesheet" href="https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/style.min.css">
    <style>
        body { margin: 0; display: flex; height: 100vh; font-family: sans-serif; }
        #sidebar { width: 320px; background: #f8f9fa; padding: 20px; border-right: 1px solid #ddd; }
        #viewer-container { flex-grow: 1; background: #111; }
        .comment-box { background: white; padding: 10px; margin-top: 10px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div id="sidebar">
        <h4>3D Workspace Feedback</h4>
        <textarea id="commentText" class="form-control w-100 mb-2" placeholder="Type spatial comment..."></textarea>
        <button onclick="submitSpatialComment()" class="btn btn-primary w-100">Submit Feedback</button>
        <hr>
        <h5>Review Markers</h5>
        <div id="commentsList"></div>
    </div>
    <div id="viewer-container"></div>

    <script src="https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/viewer3D.min.js"></script>
    <script th:inline="javascript">
        const documentId = 'urn:' + [[${urn}]];
        const token = [[${accessToken}]];
        const drawingId = [[${drawingId}]];
        let viewer;

        Autodesk.Viewing.Initializer({ env: 'AutodeskProduction', api: 'derivativeV2', getAccessToken: (cb) => cb(token, 3600) }, () => {
            viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('viewer-container'));
            viewer.start();
            Autodesk.Viewing.Document.load(documentId, (doc) => viewer.loadDocumentNode(doc, doc.getRoot().getDefaultGeometry()), console.error);
            loadSavedComments();
        });

        function submitSpatialComment() {
            const text = document.getElementById('commentText').value;
            if (!text.trim()) return;
            fetch('/api/comments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ drawingId, commentText: text, cameraState: JSON.stringify(viewer.getState()), dbId: viewer.getSelection()[0] || null })
            }).then(() => { document.getElementById('commentText').value = ''; loadSavedComments(); });
        }

        function loadSavedComments() {
            fetch(`/api/comments/drawing/${drawingId}`).then(res => res.json()).then(comments => {
                const list = document.getElementById('commentsList');
                list.innerHTML = '';
                comments.forEach(c => {
                    const el = document.createElement('div');
                    el.className = 'comment-box';
                    el.innerHTML = `p>${c.commentText}</p><button class="btn btn-sm btn-secondary" onclick='viewer.restoreState(${c.cameraState})'>Inspect Camera</button>`;
                    list.appendChild(el);
                });
            });
        }
    </script>
</body>
</html>'''
}

for path, code in project_structure.items():
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

print("Project generation script ready.")
