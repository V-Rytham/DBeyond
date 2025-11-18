from flask import Flask, render_template, request, jsonify
import sqlite3
import time
import json
from quantum_optimizer import QuantumQueryOptimizer

app = Flask(__name__)

class QueryExecutor:
    def __init__(self, db_path='database/sample.db'):
        self.db_path = db_path
    
    def execute_query(self, query, join_order=None):
        """Execute SQL query with optional join order hint"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_time = time.time()
        
        try:
            # If join order is specified, we'd normally use query hints
            # For SQLite, we'll simulate this by analyzing the execution
            if join_order:
                print(f"Executing with forced join order: {join_order}")
                # In a real database, you'd use query hints like:
                # SELECT /*+ ORDERED */ ... for Oracle
                # or use join hints in other databases
            
            cursor.execute(query)
            results = cursor.fetchall()
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'results': results[:10],  # Limit for display
                'row_count': len(results),
                'execution_time': execution_time,
                'columns': [description[0] for description in cursor.description]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
        finally:
            conn.close()

# Global instances
query_executor = QueryExecutor()
quantum_optimizer = QuantumQueryOptimizer(use_real_hardware=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-classical', methods=['POST'])
def execute_classical():
    data = request.json
    query = data.get('query', '')
    
    print(f"Executing classical query: {query}")
    
    result = query_executor.execute_query(query)
    
    # Add join order information (simulated)
    result['join_order'] = "Classical Optimizer Choice"
    
    return jsonify(result)

@app.route('/execute-quantum', methods=['POST'])
def execute_quantum():
    data = request.json
    query = data.get('query', '')
    
    print(f"Executing quantum-optimized query: {query}")
    
    try:
        # Step 1: Get quantum optimization recommendation
        quantum_result = quantum_optimizer.optimize_query(query)
        recommended_order = quantum_result['join_order']
        
        # Step 2: Execute query with quantum recommendation
        # In a real system, you'd use database-specific hints
        # For this demo, we'll simulate the execution
        
        result = query_executor.execute_query(query, join_order=recommended_order)
        
        # Add quantum analysis information
        result['quantum_recommendation'] = quantum_result
        result['join_order'] = ' → '.join(recommended_order)
        result['confidence'] = quantum_result['confidence']
        result['quantum_analysis'] = {
            'recommended_join_order': ' → '.join(recommended_order),
            'predicted_cost': quantum_result['predicted_cost'],
            'confidence': quantum_result['confidence'],
            'all_considered_orders': {
                str(k): {'order': ' → '.join(v['order']), 'cost': v['cost']} 
                for k, v in quantum_result['all_orders'].items()
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Quantum optimization failed: {str(e)}"
        })

if __name__ == '__main__':
    print("🚀 Starting Quantum SQL Optimizer...")
    print("📊 Access the web interface at: http://localhost:5000")
    app.run(debug=True, port=5000)