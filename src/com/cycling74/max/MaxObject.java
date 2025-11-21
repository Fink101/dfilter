package com.cycling74.max;

/**
 * Stub for Max SDK MaxObject class
 * This allows compilation without the full Max SDK
 * Replace with actual Max SDK jar when deploying to Max for Live
 */
public class MaxObject {

    protected MaxObject() {
    }

    /**
     * Output a float value from the specified outlet
     */
    protected void outlet(int outlet, float value) {
        // Stub - actual implementation in Max SDK
        System.out.println("Outlet " + outlet + ": " + value);
    }

    /**
     * Output a string value from the specified outlet
     */
    protected void outlet(int outlet, String value) {
        // Stub - actual implementation in Max SDK
        System.out.println("Outlet " + outlet + ": " + value);
    }

    /**
     * Output an array from the specified outlet
     */
    protected void outlet(int outlet, float[] values) {
        // Stub - actual implementation in Max SDK
        System.out.println("Outlet " + outlet + ": array of " + values.length + " values");
    }

    /**
     * Post a message to the Max console
     */
    protected void post(String message) {
        System.out.println("[Max Console] " + message);
    }

    /**
     * Post an error to the Max console
     */
    protected void error(String message) {
        System.err.println("[Max Error] " + message);
    }

    /**
     * Declare outlets for the object
     */
    protected void declareOutlets(int[] types) {
        // Stub - actual implementation in Max SDK
    }

    /**
     * Declare inlets for the object
     */
    protected void declareInlets(int[] types) {
        // Stub - actual implementation in Max SDK
    }
}
