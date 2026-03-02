"""
AI Chatbot module for intelligent data analysis using Google Gemini API
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import json

# Import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def get_gemini_api_key() -> str:
    """Read and sanitize Gemini API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    api_key = api_key.strip().strip('"').strip("'")
    return api_key


def initialize_gemini():
    """Initialize Gemini API with API key"""
    if not GEMINI_AVAILABLE:
        return False

    api_key = get_gemini_api_key()
    if not api_key:
        return False

    genai.configure(api_key=api_key)
    return True


def analyze_data_with_ai(df: pd.DataFrame, question: str) -> str:
    """
    Analyze DataFrame and answer natural language questions using Google Gemini API
    
    Args:
        df: Pandas DataFrame to analyze
        question: User's natural language question
        
    Returns:
        str: AI-generated answer from Gemini
    """
    
    # Try Gemini API first
    if GEMINI_AVAILABLE and initialize_gemini():
        try:
            return gemini_analysis(df, question)
        except Exception as e:
            error_message = str(e)
            if "API_KEY_INVALID" in error_message or "API key not valid" in error_message:
                fallback = intelligent_data_analysis(df, question)
                return (
                    "Gemini API key is invalid. Update GEMINI_API_KEY in .env with a fresh key from "
                    "https://aistudio.google.com/app/apikey.\n\n"
                    f"Fallback analysis:\n{fallback}"
                )
            print(f"Gemini API error: {error_message}")
    
    # Fallback: Intelligent keyword-based analysis
    return intelligent_data_analysis(df, question)


def gemini_analysis(df: pd.DataFrame, question: str) -> str:
    """
    Use Google Gemini API to analyze data and answer questions
    """
    try:
        # Prepare data summary for Gemini
        data_summary = prepare_data_summary(df)
        
        # Create the prompt for Gemini
        prompt = f"""You are a data analysis expert. I have a dataset with the following information:

{data_summary}

The user asks: {question}

Please provide a clear, concise answer based on the data. If the answer requires calculations, show your work. If the data doesn't contain relevant information, say so clearly."""
        
        # Initialize the model (choose a model that is currently available for this API key)
        model_candidates = [
            'models/gemini-2.0-flash',
            'models/gemini-2.5-flash',
            'models/gemini-flash-latest',
        ]

        last_error = None
        response = None
        for model_name in model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                break
            except Exception as model_error:
                last_error = model_error

        if response is None:
            raise RuntimeError(str(last_error) if last_error else "No Gemini model response")
        
        return response.text
        
    except Exception as e:
        raise RuntimeError(str(e))


def prepare_data_summary(df: pd.DataFrame) -> str:
    """Prepare a comprehensive summary for Gemini"""
    summary = f"""
Dataset Overview:
- Shape: {df.shape[0]} rows, {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}

Data Types:
{df.dtypes.to_string()}

First few rows:
{df.head(3).to_string()}

Numeric Summary:
{df.describe().to_string()}

Missing Values:
{df.isnull().sum().to_string()}
"""
    return summary


def intelligent_data_analysis(df: pd.DataFrame, question: str) -> str:
    """
    Intelligent fallback analysis using keyword matching and pandas operations
    """
    question_lower = question.lower()
    
    # Get basic info
    info = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'numeric_cols': df.select_dtypes(include=[np.number]).columns.tolist(),
        'object_cols': df.select_dtypes(include=['object']).columns.tolist(),
        'datetime_cols': df.select_dtypes(include=['datetime64']).columns.tolist()
    }
    
    # QUERIES ABOUT DATASET
    if any(word in question_lower for word in ['how many', 'count', 'total', 'number of']):
        return handle_count_query(df, question, info)
    
    # QUERIES ABOUT AVERAGES/MEANS
    if any(word in question_lower for word in ['average', 'mean', 'avg']):
        return handle_average_query(df, question, info)
    
    # QUERIES ABOUT TOTALS/SUMS
    if any(word in question_lower for word in ['total', 'sum', 'altogether']):
        return handle_sum_query(df, question, info)
    
    # QUERIES ABOUT MAX/MIN
    if any(word in question_lower for word in ['highest', 'lowest', 'maximum', 'minimum', 'max', 'min']):
        return handle_extrema_query(df, question, info)
    
    # QUERIES ABOUT TRENDS/TIME
    if any(word in question_lower for word in ['trend', 'over time', 'monthly', 'daily', 'yearly', 'growth']):
        return handle_trend_query(df, question, info)
    
    # QUERIES ABOUT DISTRIBUTION/STATUS
    if any(word in question_lower for word in ['distribution', 'breakdown', 'status', 'categories']):
        return handle_distribution_query(df, question, info)
    
    # QUERIES ABOUT CORRELATION/RELATIONSHIP
    if any(word in question_lower for word in ['relation', 'compare', 'relationship', 'correlation']):
        return handle_relationship_query(df, question, info)
    
    # DEFAULT: Summary statistics
    return generate_summary(df, info)


def handle_count_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle 'how many', 'count', 'total' type queries"""
    question_lower = question.lower()
    
    # Total rows
    if any(word in question_lower for word in ['rows', 'records', 'entries', 'data points', 'observations']):
        return f"The dataset contains **{len(df):,}** records/rows."
    
    # Total columns
    if any(word in question_lower for word in ['columns', 'fields', 'variables', 'features']):
        return f"The dataset has **{len(df.columns)}** columns: {', '.join(df.columns.tolist())}"
    
    # Specific column counts
    for col in info['object_cols']:
        if col.lower() in question_lower:
            unique_count = df[col].nunique()
            return f"Column '{col}' has **{unique_count}** unique values:\n" + \
                   df[col].value_counts().head(10).to_string()
    
    # Count null values
    if 'null' in question_lower or 'missing' in question_lower or 'empty' in question_lower:
        null_counts = df.isnull().sum()
        result = "Missing values per column:\n"
        for col, count in null_counts[null_counts > 0].items():
            result += f"- {col}: {count}\n"
        return result if null_counts.sum() > 0 else "No missing values found!"
    
    return f"Dataset has **{len(df):,}** records with **{len(df.columns)}** columns."


def handle_average_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle average/mean queries"""
    numeric_cols = info['numeric_cols']
    
    if not numeric_cols:
        return "No numeric columns found in the dataset."
    
    results = []
    for col in numeric_cols:
        if col.lower() in question.lower() or 'all' in question.lower():
            avg_val = df[col].mean()
            results.append(f"**{col}**: {avg_val:.2f}")
    
    if results:
        return "Averages:\n- " + "\n- ".join(results)
    
    # Default: show all numeric averages
    return "Average values:\n- " + "\n- ".join([
        f"**{col}**: {df[col].mean():.2f}" for col in numeric_cols
    ])


def handle_sum_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle sum/total queries"""
    numeric_cols = info['numeric_cols']
    
    if not numeric_cols:
        return "No numeric columns found to sum."
    
    results = []
    for col in numeric_cols:
        if col.lower() in question.lower() or 'all' in question.lower():
            total = df[col].sum()
            results.append(f"**{col}**: {total:,.2f}")
    
    if results:
        return "Totals:\n- " + "\n- ".join(results)
    
    # Default: show sums
    return "Total values:\n- " + "\n- ".join([
        f"**{col}**: {df[col].sum():,.2f}" for col in numeric_cols
    ])


def handle_extrema_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle max/min queries"""
    numeric_cols = info['numeric_cols']
    
    if not numeric_cols:
        return "No numeric columns to find extrema."
    
    question_lower = question.lower()
    max_query = any(word in question_lower for word in ['highest', 'maximum', 'max', 'largest', 'best'])
    min_query = any(word in question_lower for word in ['lowest', 'minimum', 'min', 'smallest', 'worst'])
    
    results = []
    for col in numeric_cols:
        if col.lower() in question_lower or 'all' in question_lower:
            if max_query:
                max_val = df[col].max()
                results.append(f"**{col}** (MAX): {max_val:,.2f}")
            if min_query:
                min_val = df[col].min()
                results.append(f"**{col}** (MIN): {min_val:,.2f}")
    
    if results:
        return "Extrema values:\n- " + "\n- ".join(results)
    
    return "Could not determine which column to analyze."


def handle_trend_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle trend/time-based queries"""
    datetime_cols = info['datetime_cols']
    
    if not datetime_cols:
        return "No datetime columns found for trend analysis."
    
    try:
        date_col = datetime_cols[0]
        numeric_cols = info['numeric_cols']
        
        if not numeric_cols:
            return f"No numeric columns to analyze trends over {date_col}"
        
        result = f"Trends over **{date_col}**:\n"
        
        # Group by month if possible
        df_copy = df.copy()
        df_copy['month'] = pd.to_datetime(df_copy[date_col]).dt.to_period('M')
        
        for col in numeric_cols[:3]:  # Show top 3 numeric columns
            monthly = df_copy.groupby('month')[col].agg(['mean', 'count', 'sum'])
            result += f"\n**{col}**:\n"
            result += monthly.head().to_string()
        
        return result
    except Exception as e:
        return f"Could not analyze trends: {str(e)}"


def handle_distribution_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle distribution/category queries"""
    object_cols = info['object_cols']
    
    if not object_cols:
        return "No categorical columns found."
    
    results = []
    for col in object_cols[:3]:  # Top 3 categories
        if col.lower() in question.lower() or 'all' in question.lower():
            dist = df[col].value_counts()
            results.append(f"\n**{col}** Distribution:\n{dist.head().to_string()}")
    
    if results:
        return "Distribution:" + "".join(results)
    
    # Default: first categorical column
    dist = df[object_cols[0]].value_counts()
    return f"**{object_cols[0]}** Distribution:\n{dist.head(10).to_string()}"


def handle_relationship_query(df: pd.DataFrame, question: str, info: Dict) -> str:
    """Handle correlation/relationship queries"""
    numeric_cols = info['numeric_cols']
    
    if len(numeric_cols) < 2:
        return "Need at least 2 numeric columns for correlation analysis."
    
    try:
        corr_matrix = df[numeric_cols].corr()
        
        # Find strongest correlations
        result = "**Strongest Correlations**:\n"
        
        # Get upper triangle
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
        
        # Sort by absolute value
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        for col1, col2, corr in corr_pairs[:5]:
            result += f"- **{col1}** ↔ **{col2}**: {corr:.3f}\n"
        
        return result
    except Exception as e:
        return f"Could not analyze relationships: {str(e)}"


def generate_summary(df: pd.DataFrame, info: Dict) -> str:
    """Generate a comprehensive summary of the dataset"""
    summary = f"""
## Dataset Summary

**Shape**: {info['shape'][0]:,} rows × {info['shape'][1]} columns

**Columns**: {', '.join(info['columns'])}

**Data Types**:
- Numeric: {len(info['numeric_cols'])} columns
- Categorical: {len(info['object_cols'])} columns  
- DateTime: {len(info['datetime_cols'])} columns

**Basic Statistics**:
"""
    
    # Add numeric column stats
    df_describe = df[info['numeric_cols']].describe() if info['numeric_cols'] else pd.DataFrame()
    if not df_describe.empty:
        summary += "\n" + df_describe.to_string()
    
    return summary.strip()
