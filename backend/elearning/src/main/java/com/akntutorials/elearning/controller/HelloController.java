package com.akntutorials.elearning.controller;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/")
    public String hello() {
        return "✅ AKNTutorials Spring Boot App is live!";
    }
}

