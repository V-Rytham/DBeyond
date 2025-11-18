from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import time

def test_quantum_connection():
    print("🔍 Testing IBM Quantum Connection...")

    YOUR_TOKEN = "UkgyMUpF_BXZ-TrKIFmijThXdhtalER6X_c7yfX8UKTg"

    try:
        service = QiskitRuntimeService(token=YOUR_TOKEN)

        print("✅ Successfully connected to IBM Quantum!")

        real_backends = service.backends(simulator=False, operational=True)

        if real_backends:
            print(f"🎯 Found {len(real_backends)} real quantum backends:")
            for backend in real_backends:
                status = backend.status()
                print(f"   - {backend.name}: {status.status_msg} ({status.pending_jobs} jobs queued)")

            print("\n🧪 Testing actual quantum execution...")

            # 1. Create your original circuit
            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure_all()

            backend = real_backends[0]
            print(f"🚀 Target backend: {backend.name}")
            
            # 2. Transpile the circuit for the specific backend
            print("🔄 Transpiling circuit for hardware...")
            pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
            isa_circuit = pm.run(qc)  # ISA = Instruction Set Architecture
            print(f"✅ Circuit transpiled. Final gates used: {isa_circuit.count_ops()}")

            # 3. Initialize Sampler and run the TRANSPILED circuit
            sampler = SamplerV2(mode=backend)

            job = sampler.run([isa_circuit])
            job_id = job.job_id()

            print(f"📡 Job submitted successfully! Job ID: {job_id}")
            print("⏳ Waiting for results...")

            while not job.done():
                print(f"   Current status: {job.status()}")
                time.sleep(20)

            result = job.result()
            print("✅ REAL QUANTUM EXECUTION SUCCESSFUL!")
            print(f"📊 Results: {result}")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_quantum_connection()