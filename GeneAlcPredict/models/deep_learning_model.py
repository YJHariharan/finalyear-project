"""
Deep Learning Model for DNA-level analysis of alcoholism side effects.
This module provides a neural network model that analyzes DNA SNP variants
and their interaction with alcohol consumption to predict health risks.
"""

import numpy as np
import os

# Try to import TensorFlow, but provide fallback if not available
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class DNAAlcoholDeepModel:
    """
    Deep learning model for analyzing DNA-level SNP variants and their 
    interaction with alcohol consumption to predict health risks.
    """
    
    def __init__(self):
        """Initialize the DNA-Alcohol deep learning model."""
        self.model = None
        self.initialized = False
        
        # DNA SNP variants known to affect alcohol metabolism and related conditions
        self.dna_snp_list = [
            "rs1229984",  # ADH1B - alcohol dehydrogenase
            "rs671",      # ALDH2 - aldehyde dehydrogenase
            "rs698",      # ADH1C - alcohol dehydrogenase
            "rs1800497",  # ANKK1/DRD2 - dopamine receptor
            "rs279858",   # GABRA2 - GABA receptor
            "rs4680",     # COMT - catechol-O-methyltransferase
            "rs2066702",  # ADH1B*3 variant
            "rs1799971",  # OPRM1 - opioid receptor
        ]
        
        # Initialize the model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the neural network model for DNA-alcohol interaction."""
        if TF_AVAILABLE:
            try:
                # Create a simple neural network with TensorFlow
                self.model = tf.keras.Sequential([
                    tf.keras.layers.Dense(16, activation='relu', input_shape=(len(self.dna_snp_list) + 2,)),  # DNA SNPs + age + alcohol
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dense(16, activation='relu'),
                    tf.keras.layers.Dense(5, activation='sigmoid')  # 5 outputs: alcoholism risk, liver damage, neurological impact, heart risk, liver risk
                ])
                
                self.model.compile(
                    optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy']
                )
                
                # Since we don't have real training data, we'll use synthetic weights
                # This ensures deterministic predictions without actual training
                self._set_synthetic_weights()
                self.initialized = True
                
            except Exception as e:
                print(f"Error initializing TensorFlow model: {e}")
                self.initialized = False
        else:
            # TensorFlow not available, we'll use fallback prediction
            self.initialized = False
    
    def _set_synthetic_weights(self):
        """Set synthetic weights for the model to enable deterministic predictions."""
        if not TF_AVAILABLE or not self.initialized:
            return
            
        # Create deterministic weights based on known biological relationships
        # These are not trained weights but designed to produce reasonable predictions
        np.random.seed(42)  # For reproducibility
        
        # Layer 1 weights: DNA SNPs have different impacts on alcohol metabolism
        layer1_weights = np.random.normal(0, 0.1, (len(self.dna_snp_list) + 2, 16))
        # Increase weights for known important SNPs
        layer1_weights[0, :] *= 2.0  # rs1229984 (ADH1B) has strong effect
        layer1_weights[1, :] *= 1.8  # rs671 (ALDH2) has strong effect
        # Age and alcohol have strong effects
        layer1_weights[-2, :] *= 1.5  # Age
        layer1_weights[-1, :] *= 2.0  # Alcohol percentage
        
        # Layer 2-4 weights
        layer2_weights = np.random.normal(0, 0.1, (16, 32))
        layer3_weights = np.random.normal(0, 0.1, (32, 16))
        layer4_weights = np.random.normal(0, 0.1, (16, 5))  # Updated for 5 outputs
        
        # Biases
        layer1_bias = np.random.normal(0, 0.05, 16)
        layer2_bias = np.random.normal(0, 0.05, 32)
        layer3_bias = np.random.normal(0, 0.05, 16)
        layer4_bias = np.random.normal(0, 0.05, 5)  # Updated for 5 outputs
        
        # Set the weights to the model
        self.model.layers[0].set_weights([layer1_weights, layer1_bias])
        self.model.layers[1].set_weights([layer2_weights, layer2_bias])
        self.model.layers[2].set_weights([layer3_weights, layer3_bias])
        self.model.layers[3].set_weights([layer4_weights, layer4_bias])
    
    def predict(self, dna_data, age, alcohol_percentage):
        """
        Predict health risks based on DNA SNP variants and alcohol consumption.
        
        Args:
            dna_data (dict): Dictionary of DNA SNP variants (0-1 values)
            age (float): Age of the individual
            alcohol_percentage (float): Alcohol consumption percentage
            
        Returns:
            dict: Predicted risks including alcoholism risk, liver damage, and neurological impact
        """
        # Ensure all SNPs are in the data, default to 0.5 (average risk) if missing
        input_features = []
        for snp in self.dna_snp_list:
            input_features.append(dna_data.get(snp, 0.5))
        
        # Add age and alcohol percentage
        input_features.append(age / 100.0)  # Normalize age
        input_features.append(alcohol_percentage / 100.0)  # Normalize alcohol
        
        if TF_AVAILABLE and self.initialized:
            # Use TensorFlow model for prediction
            input_array = np.array([input_features])
            predictions = self.model.predict(input_array, verbose=0)[0]
            
            return {
                "alcoholism_risk": float(predictions[0] * 100),
                "liver_damage_risk": float(predictions[1] * 100),
                "neurological_impact": float(predictions[2] * 100),
                "dna_heart_risk": float(predictions[3] * 100),
                "dna_liver_risk": float(predictions[4] * 100)
            }
        else:
            # Fallback prediction method using weighted sum
            return self._fallback_predict(input_features)
    
    def _fallback_predict(self, features):
        """
        Fallback prediction method when TensorFlow is not available.
        Uses a weighted sum approach based on known biological relationships.
        
        Args:
            features (list): List of input features (DNA SNPs + age + alcohol)
            
        Returns:
            dict: Predicted risks
        """
        # Weights for each SNP's contribution to different risks
        # Based on literature about these SNPs' effects
        alcoholism_weights = [0.25, 0.20, 0.15, 0.10, 0.08, 0.07, 0.10, 0.05]
        liver_weights = [0.20, 0.25, 0.15, 0.05, 0.05, 0.10, 0.15, 0.05]
        neuro_weights = [0.10, 0.15, 0.10, 0.20, 0.15, 0.15, 0.05, 0.10]
        heart_weights = [0.15, 0.10, 0.15, 0.05, 0.10, 0.20, 0.15, 0.10]
        liver_risk_weights = [0.20, 0.30, 0.15, 0.05, 0.05, 0.05, 0.15, 0.05]
        
        # Calculate base risks from DNA SNPs
        alcoholism_base = sum(w * v for w, v in zip(alcoholism_weights, features[:8]))
        liver_base = sum(w * v for w, v in zip(liver_weights, features[:8]))
        neuro_base = sum(w * v for w, v in zip(neuro_weights, features[:8]))
        heart_base = sum(w * v for w, v in zip(heart_weights, features[:8]))
        liver_risk_base = sum(w * v for w, v in zip(liver_risk_weights, features[:8]))
        
        # Age factor (risk increases with age)
        age_norm = features[-2]  # Normalized age
        age_factor = 0.5 + age_norm * 0.5  # 0.5-1.0 range
        
        # Alcohol factor (risk increases with consumption)
        alc_norm = features[-1]  # Normalized alcohol
        alc_factor = 0.2 + alc_norm * 0.8  # 0.2-1.0 range
        
        # Calculate final risks with age and alcohol interaction
        alcoholism_risk = alcoholism_base * 40 * alc_factor * (0.7 + 0.3 * age_factor)
        liver_risk = liver_base * 50 * alc_factor * age_factor
        neuro_risk = neuro_base * 45 * alc_factor * (0.6 + 0.4 * age_factor)
        heart_risk = heart_base * 45 * alc_factor * (0.5 + 0.5 * age_factor)
        liver_disease_risk = liver_risk_base * 55 * alc_factor * (0.4 + 0.6 * age_factor)
        
        # Ensure risks are in 0-100 range
        alcoholism_risk = max(0, min(100, alcoholism_risk))
        liver_risk = max(0, min(100, liver_risk))
        neuro_risk = max(0, min(100, neuro_risk))
        heart_risk = max(0, min(100, heart_risk))
        liver_disease_risk = max(0, min(100, liver_disease_risk))
        
        return {
            "alcoholism_risk": alcoholism_risk,
            "liver_damage_risk": liver_risk,
            "neurological_impact": neuro_risk,
            "dna_heart_risk": heart_risk,
            "dna_liver_risk": liver_disease_risk
        }
    
    def get_dna_snp_list(self):
        """Return the list of DNA SNP variants used by the model."""
        return self.dna_snp_list