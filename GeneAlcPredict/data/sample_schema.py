"""
Sample data schema and validation rules for the DNA alcoholism effects analyzer
"""

# Required input fields with their types and descriptions
REQUIRED_FIELDS = {
    'age': {
        'type': 'integer',
        'range': (18, 100),
        'description': 'Patient age in years'
    },
    'alcohol_percentage': {
        'type': 'float',
        'range': (0, 100),
        'description': 'Daily alcohol consumption as percentage of total fluid intake'
    }
}

# Optional input fields
OPTIONAL_FIELDS = {
    'gender': {
        'type': 'categorical',
        'options': ['Male', 'Female', 'Other'],
        'default': 'Male',
        'description': 'Patient gender'
    },
    'years_drinking': {
        'type': 'integer',
        'range': (0, 80),
        'default': 5,
        'description': 'Number of years of regular alcohol consumption'
    },
    'aldh2_variant': {
        'type': 'categorical',
        'options': ['Normal', 'Heterozygous', 'Homozygous Deficient'],
        'default': 'Normal',
        'description': 'ALDH2 gene variant affecting alcohol metabolism'
    },
    'cyp2e1_activity': {
        'type': 'float',
        'range': (0, 3.0),
        'default': 1.0,
        'description': 'CYP2E1 enzyme activity level (relative to normal)'
    },
    'dna_methylation': {
        'type': 'float',
        'range': (0, 1.0),
        'default': 0.5,
        'description': 'DNA methylation score (0=low, 1=high)'
    },
    'oxidative_stress': {
        'type': 'float',
        'range': (0, 20.0),
        'default': 3.0,
        'description': 'Oxidative stress markers level'
    },
    'apoe_variant': {
        'type': 'categorical',
        'options': ['ε2/ε2', 'ε2/ε3', 'ε2/ε4', 'ε3/ε3', 'ε3/ε4', 'ε4/ε4'],
        'default': 'ε3/ε3',
        'description': 'APOE gene variant'
    },
    'family_history': {
        'type': 'multi_select',
        'options': ['Heart Disease', 'Liver Disease', 'Kidney Disease', 'Alcoholism'],
        'default': [],
        'description': 'Family history of relevant conditions'
    },
    'lifestyle_score': {
        'type': 'integer',
        'range': (0, 10),
        'default': 5,
        'description': 'Overall lifestyle health score (0=poor, 10=excellent)'
    },
    'bmi': {
        'type': 'float',
        'range': (10, 60),
        'default': 25.0,
        'description': 'Body Mass Index'
    }
}

# Output schema for predictions
OUTPUT_SCHEMA = {
    'heart_disease_risk': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Probability of developing heart disease'
    },
    'liver_disease_risk': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Probability of developing liver disease'
    },
    'kidney_disease_risk': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Probability of developing kidney disease'
    }
}

# Confidence score schema
CONFIDENCE_SCHEMA = {
    'heart': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Confidence level for heart disease prediction'
    },
    'liver': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Confidence level for liver disease prediction'
    },
    'kidney': {
        'type': 'float',
        'range': (0, 1.0),
        'description': 'Confidence level for kidney disease prediction'
    }
}

# Sample CSV format for batch upload
SAMPLE_CSV_HEADERS = [
    'age', 'gender', 'alcohol_percentage', 'years_drinking',
    'aldh2_variant', 'cyp2e1_activity', 'dna_methylation',
    'oxidative_stress', 'apoe_variant', 'lifestyle_score', 'bmi'
]

# Risk level thresholds
RISK_THRESHOLDS = {
    'low': 0.3,
    'moderate': 0.5,
    'high': 0.7
}

# Feature importance categories
FEATURE_CATEGORIES = {
    'demographic': ['age', 'gender', 'bmi'],
    'alcohol_exposure': ['alcohol_percentage', 'years_drinking'],
    'genetic': ['aldh2_variant', 'cyp2e1_activity', 'apoe_variant'],
    'biomarkers': ['dna_methylation', 'oxidative_stress'],
    'lifestyle': ['lifestyle_score'],
    'family_history': ['family_history']
}

# Disease-specific risk factors
DISEASE_RISK_FACTORS = {
    'heart_disease': {
        'primary': ['age', 'alcohol_percentage', 'apoe_variant'],
        'secondary': ['gender', 'bmi', 'lifestyle_score'],
        'genetic': ['aldh2_variant', 'family_history']
    },
    'liver_disease': {
        'primary': ['alcohol_percentage', 'years_drinking', 'aldh2_variant'],
        'secondary': ['age', 'cyp2e1_activity', 'dna_methylation'],
        'genetic': ['aldh2_variant', 'family_history']
    },
    'kidney_disease': {
        'primary': ['age', 'alcohol_percentage', 'oxidative_stress'],
        'secondary': ['bmi', 'lifestyle_score'],
        'genetic': ['family_history']
    }
}

def get_field_info(field_name):
    """Get information about a specific field"""
    if field_name in REQUIRED_FIELDS:
        return REQUIRED_FIELDS[field_name]
    elif field_name in OPTIONAL_FIELDS:
        return OPTIONAL_FIELDS[field_name]
    else:
        return None

def validate_field_value(field_name, value):
    """Validate a field value against its schema"""
    field_info = get_field_info(field_name)
    
    if not field_info:
        return False, f"Unknown field: {field_name}"
    
    field_type = field_info['type']
    
    try:
        if field_type == 'integer':
            value = int(value)
            min_val, max_val = field_info['range']
            if not (min_val <= value <= max_val):
                return False, f"{field_name} must be between {min_val} and {max_val}"
        
        elif field_type == 'float':
            value = float(value)
            min_val, max_val = field_info['range']
            if not (min_val <= value <= max_val):
                return False, f"{field_name} must be between {min_val} and {max_val}"
        
        elif field_type == 'categorical':
            if value not in field_info['options']:
                return False, f"{field_name} must be one of: {field_info['options']}"
        
        elif field_type == 'multi_select':
            if not isinstance(value, list):
                return False, f"{field_name} must be a list"
            for item in value:
                if item not in field_info['options']:
                    return False, f"Invalid option '{item}' for {field_name}"
    
    except (ValueError, TypeError):
        return False, f"Invalid data type for {field_name}"
    
    return True, "Valid"

def get_default_values():
    """Get default values for all optional fields"""
    defaults = {}
    for field_name, field_info in OPTIONAL_FIELDS.items():
        if 'default' in field_info:
            defaults[field_name] = field_info['default']
    return defaults

def generate_sample_data(n_samples=5):
    """Generate sample data for testing"""
    import random
    
    samples = []
    
    for i in range(n_samples):
        sample = {
            'age': random.randint(25, 70),
            'gender': random.choice(['Male', 'Female']),
            'alcohol_percentage': round(random.uniform(0.5, 15), 1),
            'years_drinking': random.randint(1, 30),
            'aldh2_variant': random.choice(['Normal', 'Heterozygous', 'Homozygous Deficient']),
            'cyp2e1_activity': round(random.uniform(0.5, 2.0), 1),
            'dna_methylation': round(random.uniform(0.2, 0.8), 2),
            'oxidative_stress': round(random.uniform(1.0, 8.0), 1),
            'apoe_variant': random.choice(['ε2/ε3', 'ε3/ε3', 'ε3/ε4']),
            'lifestyle_score': random.randint(3, 8),
            'bmi': round(random.uniform(20, 35), 1)
        }
        samples.append(sample)
    
    return samples
