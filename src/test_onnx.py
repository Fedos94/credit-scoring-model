import onnxruntime as ort
print("ONNX Runtime импортирован успешно!")
print(f"Версия: {ort.__version__}")
print(f"Доступные провайдеры: {ort.get_available_providers()}")