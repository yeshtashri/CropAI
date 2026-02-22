/**
 * app.js — AI Crop Disease Prediction System
 * Handles: drag-and-drop upload, file validation, image preview,
 *          form submission with loading overlay, confidence bar animation.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Element references ─────────────────────────────────────────────────
  const uploadZone      = document.getElementById('upload-zone');
  const fileInput       = document.getElementById('file-input');
  const previewContainer= document.getElementById('preview-container');
  const previewImg      = document.getElementById('preview-img');
  const uploadPrompt    = document.getElementById('upload-prompt');
  const analyzeBtn      = document.getElementById('analyze-btn');
  const uploadForm      = document.getElementById('upload-form');
  const loadingOverlay  = document.getElementById('loading-overlay');
  const selectedName    = document.getElementById('selected-name');
  const removeBtn       = document.getElementById('remove-btn');

  const ALLOWED_TYPES   = ['image/jpeg', 'image/jpg', 'image/png',
                            'image/bmp', 'image/webp'];
  const MAX_SIZE_MB     = 16;

  // ── Drag-and-Drop ──────────────────────────────────────────────────────
  if (uploadZone) {
    ['dragenter', 'dragover'].forEach(evt => {
      uploadZone.addEventListener(evt, e => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('drag-over');
      });
    });

    ['dragleave', 'drop'].forEach(evt => {
      uploadZone.addEventListener(evt, e => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('drag-over');
      });
    });

    uploadZone.addEventListener('drop', e => {
      const files = e.dataTransfer.files;
      if (files.length > 0) handleFile(files[0]);
    });

    // Click on zone → trigger hidden file input
    uploadZone.addEventListener('click', e => {
      if (e.target !== removeBtn && !removeBtn?.contains(e.target)) {
        fileInput?.click();
      }
    });
  }

  // ── File input change ──────────────────────────────────────────────────
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
    });
  }

  // ── Handle selected file ───────────────────────────────────────────────
  function handleFile(file) {
    // Validate type
    if (!ALLOWED_TYPES.includes(file.type)) {
      showToast('⚠️ Invalid file type. Please upload a JPG or PNG image.', 'warning');
      return;
    }

    // Validate size
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > MAX_SIZE_MB) {
      showToast(`⚠️ File too large (${sizeMB.toFixed(1)} MB). Max size is ${MAX_SIZE_MB} MB.`, 'warning');
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = e => {
      if (previewImg) previewImg.src = e.target.result;
      if (previewContainer) previewContainer.style.display = 'block';
      if (uploadPrompt) uploadPrompt.style.display = 'none';
      if (selectedName) selectedName.textContent = file.name;
    };
    reader.readAsDataURL(file);

    // Inject file into the actual form input
    const dt = new DataTransfer();
    dt.items.add(file);
    if (fileInput) fileInput.files = dt.files;

    // Enable analyze button
    if (analyzeBtn) {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm d-none" id="btn-spinner"></span> 🔍 Analyze Disease';
    }
  }

  // ── Remove / reset selection ───────────────────────────────────────────
  if (removeBtn) {
    removeBtn.addEventListener('click', e => {
      e.stopPropagation();
      resetUpload();
    });
  }

  function resetUpload() {
    if (fileInput)        fileInput.value = '';
    if (previewContainer) previewContainer.style.display = 'none';
    if (uploadPrompt)     uploadPrompt.style.display = 'block';
    if (analyzeBtn)       analyzeBtn.disabled = true;
    if (selectedName)     selectedName.textContent = '';
  }

  // ── Form submit → show loading overlay ────────────────────────────────
  if (uploadForm) {
    uploadForm.addEventListener('submit', e => {
      if (!fileInput || fileInput.files.length === 0) {
        e.preventDefault();
        showToast('Please select an image before analyzing.', 'warning');
        return;
      }

      // Show spinner inside button
      const spinner = document.getElementById('btn-spinner');
      if (spinner) spinner.classList.remove('d-none');
      if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
      }

      // Show full-screen loading overlay
      if (loadingOverlay) loadingOverlay.classList.add('active');
    });
  }

  // ── Confidence bar animation (result page) ─────────────────────────────
  const confidenceFill = document.querySelector('.confidence-bar-fill');
  if (confidenceFill) {
    const targetWidth = confidenceFill.getAttribute('data-width') || '0';
    // Start from 0 then animate to target
    confidenceFill.style.width = '0%';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      confidenceFill.style.width = targetWidth + '%';
    }));
  }

  // ── Auto-dismiss alerts ────────────────────────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity .5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // ── Toast notifications ────────────────────────────────────────────────
  function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container')
                   || createToastContainer();
    const colors = {
      warning: '#fbbf24',
      danger : '#f87171',
      success: '#5dba7d',
      info   : '#60a5fa',
    };
    const toast = document.createElement('div');
    toast.style.cssText = `
      background: #1c2330;
      border: 1px solid ${colors[type] || colors.info}44;
      color: ${colors[type] || colors.info};
      padding: .75rem 1.25rem;
      border-radius: 10px;
      margin-bottom: .5rem;
      font-size: .9rem;
      box-shadow: 0 4px 20px rgba(0,0,0,.4);
      animation: slideInRight .3s ease;
      max-width: 340px;
    `;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.transition = 'opacity .4s';
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }

  function createToastContainer() {
    const c = document.createElement('div');
    c.id = 'toast-container';
    c.style.cssText = `
      position: fixed;
      top: 80px;
      right: 1rem;
      z-index: 99999;
    `;
    document.body.appendChild(c);
    return c;
  }

  // ── Add keyframes for toast ────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from { opacity:0; transform: translateX(30px); }
      to   { opacity:1; transform: translateX(0); }
    }
  `;
  document.head.appendChild(style);

});
