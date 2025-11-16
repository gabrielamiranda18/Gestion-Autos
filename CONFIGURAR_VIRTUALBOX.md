# 🚀 Guía Rápida: Optimizar VirtualBox para AutoGest

## Problema Detectado

Tu VM de Fedora está usando **1.3GB de SWAP** y **renderizado por software**, lo que causa lentitud extrema.

## ✅ Solución en 3 Pasos

### 1️⃣ Aumentar RAM de la VM

**Desde VirtualBox (con la VM apagada):**

1. Abre VirtualBox
2. Selecciona tu VM de Fedora
3. Clic en **"Configuración"** (Settings)
4. Ve a **"Sistema"** (System)
5. En la pestaña **"Placa base"** (Motherboard):
   - Aumenta "Memoria base" a **6144 MB** (6GB) o al menos **4096 MB** (4GB)
6. Clic en **"Aceptar"**

### 2️⃣ Activar Aceleración 3D

**Desde VirtualBox (con la VM apagada):**

1. En **"Configuración"** > **"Pantalla"** (Display)
2. En la pestaña **"Pantalla"**:
   - Memoria de video: **128 MB**
   - Controlador gráfico: **VMSVGA** o **VBoxVGA**
   - ✅ Marcar **"Habilitar aceleración 3D"** (Enable 3D Acceleration)
3. Clic en **"Aceptar"**

### 3️⃣ Optimizar CPUs (Opcional pero Recomendado)

1. En **"Configuración"** > **"Sistema"**
2. Pestaña **"Procesador"**:
   - Procesadores: **2** (mínimo) o **4** (óptimo)
   - ✅ Marcar **"Habilitar PAE/NX"**
   - ✅ Marcar **"Habilitar VT-x/AMD-V anidado"** (si disponible)
3. Clic en **"Aceptar"**

## 🔧 Configuración Óptima Recomendada

| Recurso | Mínimo | Recomendado | Tu Actual |
|---------|--------|-------------|-----------|
| RAM | 4GB | 6-8GB | 5.6GB (pero usando SWAP) |
| CPUs | 2 cores | 4 cores | ✅ 4 cores |
| Video RAM | 64MB | 128MB | ? |
| Aceleración 3D | ❌ | ✅ | ❌ Desactivada |

## 🎯 Resultado Esperado

Después de aplicar estos cambios:

- ✅ SWAP = 0 MB (sin uso de disco como memoria)
- ✅ Renderizado acelerado por hardware
- ✅ UI fluida y rápida
- ✅ Carga de imágenes instantánea (desde caché)

## 📝 Instrucciones Paso a Paso con Imágenes

### Cómo aumentar RAM:

```
VirtualBox > Tu VM > Configuración > Sistema > Placa Base
┌─────────────────────────────────────────┐
│ Memoria base: [========] 6144 MB        │
│                                         │
│ (Arrastra el slider a 6144)             │
└─────────────────────────────────────────┘
```

### Cómo activar aceleración 3D:

```
VirtualBox > Tu VM > Configuración > Pantalla
┌─────────────────────────────────────────┐
│ Memoria de video: [====] 128 MB         │
│                                         │
│ ☑ Habilitar aceleración 3D              │
│ Controlador gráfico: VMSVGA             │
└─────────────────────────────────────────┘
```

## ⚡ Optimizaciones Adicionales en Fedora

Una vez iniciada la VM con la nueva configuración:

```bash
# 1. Deshabilitar animaciones (opcional, mejora fluidez)
gsettings set org.gnome.desktop.interface enable-animations false

# 2. Verificar mejoras
./diagnostico_rendimiento.sh

# 3. Iniciar aplicación
./run.sh
```

## 🆘 Si Sigues con Problemas

1. **Reinicia la VM** después de cambiar la configuración
2. Verifica que tu PC físico tenga suficiente RAM libre (al menos 8GB total)
3. Cierra aplicaciones pesadas en el host (Chrome, etc.)
4. Si usas Windows como host, desactiva Hyper-V

## 📊 Verificar Mejoras

Después de reiniciar la VM:

```bash
cd ~/Documents/Gestion-Autos
./diagnostico_rendimiento.sh
```

Deberías ver:
- ✅ Swap en Uso: 0 MB (o muy bajo)
- ✅ Aceleración de hardware activa

---

**Nota:** Estos cambios requieren **reiniciar la VM** para tener efecto.
