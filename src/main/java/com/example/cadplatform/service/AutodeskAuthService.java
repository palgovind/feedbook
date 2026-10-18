package com.example.cadplatform.service;

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
}