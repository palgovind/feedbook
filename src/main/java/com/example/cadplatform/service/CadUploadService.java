package com.example.cadplatform.service;

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

        String jsonPayload = "{"input": {"urn": "" + base64Urn + "" }, "output": {"formats": [{"type": "svf2", "views": ["2d", "3d"]}]}}";
        webClient.post().uri("/modelderivative/v2/designdata/job")
                .header("Authorization", "Bearer " + token)
                .header("Content-Type", "application/json")
                .bodyValue(jsonPayload).retrieve().toBodilessEntity().block();

        Drawing drawing = new Drawing();
        drawing.setTitle(title);
        drawing.setApsUrn(base64Urn);
        return drawingRepository.save(drawing);
    }
}