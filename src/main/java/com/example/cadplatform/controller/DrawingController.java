package com.example.cadplatform.controller;

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
}