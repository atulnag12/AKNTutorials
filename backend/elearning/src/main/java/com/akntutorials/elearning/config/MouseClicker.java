package com.akntutorials.elearning.config;

import java.awt.*;
import java.awt.event.InputEvent;

public class MouseClicker {
    public static void main(String[] args) throws AWTException, InterruptedException {
        Robot robot = new Robot();

        // Wait 3 seconds so you can switch to the target window
        Thread.sleep(3000);

        // Move mouse to (x=600, y=400) — change this as per your screen
        robot.mouseMove(600, 400);

        // Left mouse click
        robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
        robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);

        System.out.println("Mouse clicked at (600, 400)");
    }
}
