package com.example.cadplatform.model;

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
}