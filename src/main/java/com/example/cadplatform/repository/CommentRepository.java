package com.example.cadplatform.repository;

import com.example.cadplatform.model.DrawingComment;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface CommentRepository extends JpaRepository<DrawingComment, Long> {
    List<DrawingComment> findByDrawingIdOrderByCreatedAtDesc(Long drawingId);
}