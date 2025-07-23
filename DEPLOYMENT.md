# Streamlit Cloud Deployment Guide

## Quick Deployment

1. **Fork or clone this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Connect your GitHub account** and select this repository
4. **Set the main file path** to: `web_app_streamlit.py`
5. **Set the requirements file** to: `requirements_streamlit.txt`
6. **Click Deploy**

## File Structure for Streamlit Cloud

```
image_comparison_tool/
├── web_app_streamlit.py      # Main Streamlit app (use this for deployment)
├── requirements_streamlit.txt # Dependencies (no OpenCV)
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── main.py                  # CLI version (local use only)
├── web_app.py              # Original web app (local use only)
├── requirements.txt        # Full dependencies (local use only)
└── README.md              # Documentation
```

## Key Changes for Streamlit Cloud

### 1. **No OpenCV Dependency**
- The Streamlit Cloud version uses PIL (Pillow) instead of OpenCV
- This avoids system-level dependency issues on Streamlit Cloud

### 2. **Streamlit-Compatible Requirements**
- `requirements_streamlit.txt` contains only cloud-compatible packages
- Excludes OpenCV which causes deployment issues

### 3. **Self-Contained Functions**
- All image processing functions are included in the main file
- No external dependencies on OpenCV-specific functions

## Troubleshooting

### Common Issues:

1. **OpenCV Import Error**
   - **Solution**: Use `web_app_streamlit.py` instead of `web_app.py`
   - **Reason**: OpenCV has system dependencies not available on Streamlit Cloud

2. **Memory Issues**
   - **Solution**: The app automatically resizes large images
   - **Limit**: Recommended image size < 10MB each

3. **Deployment Fails**
   - **Check**: Ensure you're using `web_app_streamlit.py` as main file
   - **Check**: Use `requirements_streamlit.txt` for dependencies

### Local vs Cloud Usage:

| Feature | Local (web_app.py) | Cloud (web_app_streamlit.py) |
|---------|-------------------|------------------------------|
| OpenCV Support | ✅ Full | ❌ None |
| PIL Support | ✅ Full | ✅ Full |
| Performance | ⚡ Fast | 🐌 Slower |
| Deployment | ❌ Issues | ✅ Works |
| Features | 🎯 Complete | 🎯 Complete |

## Testing Locally

To test the Streamlit Cloud version locally:

```bash
# Install cloud-compatible dependencies
pip install -r requirements_streamlit.txt

# Run the cloud-compatible version
streamlit run web_app_streamlit.py
```

## Performance Notes

- **Image Processing**: Slightly slower than OpenCV version
- **Memory Usage**: More efficient for large images
- **Compatibility**: Works on all platforms including Streamlit Cloud

## Support

If you encounter issues:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Verify file paths** are correct
3. **Ensure requirements** are properly specified
4. **Test locally** first with `web_app_streamlit.py` 