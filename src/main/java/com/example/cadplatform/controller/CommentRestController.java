package com.example.cadplatform.controller;

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
}