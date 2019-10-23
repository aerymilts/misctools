import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Input and output filenames for processing digibot logs.')
parser.add_argument('input', type=str, 
                    help='input file')
parser.add_argument('output', type=str,
                    help='output file')

args = parser.parse_args()

read_file = args.input
write_file = args.output

def series_separate_by_types(row):
    """
    Assign values to columns based on type inferred from partial string matches 
    and fill nans otherwise.
    """
    points = None
    cost = None
    transaction = None
    card = None
    date = None
    
    try:
        date = pd.to_datetime(row, format='%d/%m/%Y')
    except:
        pass
    
    if date:
        return date, points, cost, transaction, card
    elif 'DBS Points' in row:
        points = row
    elif 'S$' in row:
        cost = row
    elif 'Card' in row:
        card = row
    else:
        transaction = row
        
    return date, points, cost, transaction, card

def format_logs(df):
    """
    Align log values and drop nans, dtype casting where applicable and sort by date in ascending order.
    """
    data = df['default'].apply(series_separate_by_types).apply(pd.Series)
    new_cols = ['date', 'points', 'cost', 'transaction', 'card']
    data = data.rename(columns={c: cn for c, cn in zip(data.columns, new_cols)})

    for c in data.columns:
        print(data[c].notnull().value_counts())

    for col in data:
        data[col] = data[col][data[col].notnull()].reset_index(drop=True)

    data = data[data.notnull().any(axis=1)]
    data['date'] = pd.to_datetime(data['date'][data['date'].notnull()]).reset_index(drop=True)
    data['points'] = data['points'].apply(lambda r: r.split(' ')[0]).astype(int)
    data['cost'] = data['cost'].str.extract('S\$(.*)', expand=False).astype(float)

    data = data.sort_values('date').reset_index(drop=True)
    
    return data

if __name__ == '__main__':
    df = pd.read_csv(read_file, sep='\t', names=['default'])
    data = format_logs(df)
    data.to_csv(write_file, index=False)