package com.example.cadplatform.dto;

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
}