package com.example.cadplatform.controller;

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
}