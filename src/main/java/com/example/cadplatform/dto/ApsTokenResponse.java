package com.example.cadplatform.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ApsTokenResponse {
    @JsonProperty("access_token") private String accessToken;
    @JsonProperty("token_type") private String tokenType;
    @JsonProperty("expires_in") private long expiresIn;

    public String getAccessToken() { return accessToken; }
    public long getExpiresIn() { return expiresIn; }
}