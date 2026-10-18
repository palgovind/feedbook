package com.example.cadplatform.controller;

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
}