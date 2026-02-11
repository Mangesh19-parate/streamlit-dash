# Startup Funding Analysis Dashboard 💰

A comprehensive Streamlit-based analytics dashboard for exploring and analyzing startup funding data in the Indian ecosystem.

## Features

### 📊 Overall Analysis
- **Key Metrics**: Total funding, maximum investment, average funding, and number of funded startups
- **MoM Trends**: Month-over-month funding trends with toggleable metrics (Total Amount vs Deal Count)
- **Top Performers**: Lists of top-funded startups and most active investors
- **Heatmap**: Year vs Month funding distribution visualization

### 🏢 Company (Startup) POV
- **Company Profile**: Detailed information about selected startups
- **General Information**: Industry vertical, sub-industry, and location
- **Funding History**: Complete funding rounds with dates, round types, investors, and amounts
- **Similar Companies**: Recommendations based on industry vertical

### 💼 Investor POV
- **Investor Profile**: Comprehensive investor analytics
- **Key Metrics**: Recent investments and total investment amount
- **Investment Distribution**: 
  - Sector-wise breakdown (pie chart)
  - Investment stage distribution (pie chart)
  - Geographic distribution by city (pie chart)
- **YoY Trends**: Year-over-year investment patterns
- **Similar Investors**: Recommendations based on investment overlap

## Prerequisites

- Python 3.7+
- Required Python packages (see Installation)

## Installation

1. Clone the repository or download the files:
```bash
git clone <repository-url>
cd startup-funding-analysis
```

2. Install required dependencies:
```bash
pip install streamlit pandas matplotlib seaborn
```

## Data Requirements

The application expects a CSV file named `startup_cleaned.csv` in the same directory with the following columns:

- `Startup`: Name of the startup
- `date`: Funding date
- `round`: Funding round type (Seed, Series A, etc.)
- `investors`: Comma-separated list of investors
- `amount`: Funding amount in Crores (₹)
- `vertical`: Industry vertical
- `subver`: Sub-industry vertical
- `city`: Location of the startup

## Usage

1. Ensure `startup_cleaned.csv` is in the application directory

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Navigate through the dashboard using the sidebar:
   - **Overall Analysis**: View ecosystem-wide metrics and trends
   - **Company (StartUp) POV**: Explore individual startup details
   - **Investor POV**: Analyze investor portfolios and patterns

## Project Structure

```
.
├── app.py                   # Main Streamlit application
├── startup_cleaned.csv      # Dataset (required)
└── README.md               # This file
```

## Features in Detail

### Data Processing
- Automatic date parsing and temporal feature extraction (month, year)
- Handling of missing investor data with "Undisclosed" label
- Data caching for improved performance

### Visualizations
- **Line Charts**: Temporal trends and YoY analysis
- **Pie Charts**: Distribution analysis across sectors, stages, and locations
- **Heatmaps**: Cross-sectional funding patterns
- **Tables**: Detailed funding round information

### Smart Recommendations
- Similar companies based on industry vertical matching
- Similar investors based on sector overlap and investment frequency

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static visualizations
- **Seaborn**: Statistical data visualization

## Configuration

The app is configured with:
- Wide layout mode for better data visibility
- Custom page title and icon
- Data caching for optimal performance

## Future Enhancements

Potential improvements:
- Advanced filtering options
- Export functionality for reports
- Interactive plotly charts
- Machine learning-based predictions
- Investor-startup matching algorithm

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions, please open an issue in the repository.

---

**Note**: Ensure your dataset is properly cleaned and formatted before running the application for best results.
