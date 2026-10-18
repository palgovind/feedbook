package com.example.cadplatform.repository;

import com.example.cadplatform.model.Drawing;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface DrawingRepository extends JpaRepository<Drawing, Long> {
    List<Drawing> findAllByOrderByCreatedAtDesc();
}