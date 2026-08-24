/**
 * Modal Components for X-ELRA
 *
 * Handles note/feedback modal and related functionality.
 */

import { api } from '../services/api.js';
import { showToast } from './ui.js';
import { errorMessage } from '../utils/helpers.js';

// Sentiment prefix pattern for parsing feedback notes
const SENTIMENT_PREFIX_RE = /^\s*\[(positive|neutral|negative)\]\s*/i;

/**
 * Parse a feedback note to extract sentiment and body
 * @param {string} raw - Raw feedback text
 * @returns {{body: string, sentiment: string|null}} Parsed note
 */
export function parseFeedbackNote(raw) {
  const text = (raw || '').trim();
  if (!text) {
    return { body: '', sentiment: null };
  }
  const match = text.match(SENTIMENT_PREFIX_RE);
  if (match) {
    return {
      body: text.slice(match[0].length),
      sentiment: match[1].toLowerCase(),
    };
  }
  return { body: text, sentiment: null };
}

/**
 * Compose a feedback note with sentiment prefix
 * @param {string} body - Note body
 * @param {string|null} sentiment - Sentiment (positive/neutral/negative)
 * @returns {string} Composed note with sentiment prefix
 */
export function composeFeedbackNote(body, sentiment) {
  const trimmed = (body || '').trim();
  const prefix = sentiment ? `[${sentiment}] ` : '';
  return (prefix + trimmed).trim();
}

// Note modal state and references
let noteModalInstance = null;
let previouslyFocusedElement = null;
const noteModalRefs = {
  modal: null,
  textarea: null,
  sentimentButtons: [],
  starButtons: [],
  status: null,
  saveButton: null,
  title: null,
  charCount: null,
  ratingLabel: null,
};

const noteModalState = {
  item: null,
  learnerId: null,
  rating: 0,
  noteBody: '',
  sentiment: null,
  onSave: null,
  onClose: null,
};

const RATING_LABELS = ['', 'Not helpful', 'Needs work', 'Okay', 'Good', 'Great!'];

/**
 * Paint sentiment button states
 * @param {string|null} active - Active sentiment value
 */
function paintNoteModalSentiment(active) {
  noteModalRefs.sentimentButtons.forEach((btn) => {
    const value = btn.dataset.sent || null;
    btn.classList.toggle('active', value === active);
  });
}

/**
 * Paint star rating states
 * @param {number} rating - Current rating (1-5)
 */
function paintNoteModalStars(rating) {
  noteModalRefs.starButtons.forEach((star) => {
    const val = parseInt(star.dataset.val, 10);
    const isActive = Number.isFinite(rating) && val <= rating;
    star.classList.toggle('bi-star-fill', isActive);
    star.classList.toggle('bi-star', !isActive);
  });
  if (noteModalRefs.ratingLabel) {
    noteModalRefs.ratingLabel.textContent = RATING_LABELS[rating] || '';
  }
}

/**
 * Open the note modal for feedback entry
 * @param {Object} options - Modal options
 * @param {Object} options.item - Item being reviewed
 * @param {string} options.learnerId - Learner ID
 * @param {number} options.rating - Current rating
 * @param {string} options.noteBody - Existing note body
 * @param {string|null} options.sentiment - Current sentiment
 * @param {Function} options.onSave - Callback after save
 * @param {Function} options.onClose - Callback when modal closes (for any reason)
 */
export function openNoteModal({ item, learnerId, rating = 0, noteBody = '', sentiment = null, onSave = null, onClose = null } = {}) {
  if (!noteModalRefs.modal) {
    initNoteModal();
  }
  if (!noteModalRefs.modal) return;

  noteModalState.item = null;
  noteModalState.learnerId = null;
  noteModalState.onSave = null;
  noteModalState.onClose = null;
  noteModalState.noteBody = '';
  noteModalState.sentiment = null;
  noteModalState.rating = 0;
  if (noteModalRefs.textarea) {
    noteModalRefs.textarea.value = '';
  }
  if (noteModalRefs.charCount) {
    noteModalRefs.charCount.textContent = '0';
  }
  if (noteModalRefs.status) {
    noteModalRefs.status.textContent = '';
  }
  paintNoteModalSentiment(null);
  paintNoteModalStars(0);

  // Save the currently focused element for restoration when modal closes
  previouslyFocusedElement = document.activeElement;

  // Now set the new values
  noteModalState.item = item || null;
  noteModalState.learnerId = learnerId || null;
  noteModalState.rating = rating || 0;
  noteModalState.noteBody = noteBody || '';
  noteModalState.sentiment = sentiment || null;
  noteModalState.onSave = typeof onSave === 'function' ? onSave : null;
  noteModalState.onClose = typeof onClose === 'function' ? onClose : null;

  if (noteModalRefs.title) {
    const titleText = (item && (item.title || item.item_id)) || 'this';
    noteModalRefs.title.textContent = `Quick Review`;
  }
  if (noteModalRefs.textarea) {
    noteModalRefs.textarea.value = noteModalState.noteBody;
  }
  if (noteModalRefs.charCount) {
    noteModalRefs.charCount.textContent = (noteModalState.noteBody || '').length;
  }
  if (noteModalRefs.status) {
    noteModalRefs.status.textContent = '';
  }
  if (noteModalRefs.saveButton) {
    noteModalRefs.saveButton.disabled = false;
  }

  // Comment section is always visible (no toggle)

  paintNoteModalSentiment(noteModalState.sentiment);
  paintNoteModalStars(noteModalState.rating);

  if (noteModalInstance) {
    noteModalInstance.show();
  }

  // Don't auto-focus textarea - let user click stars first
  setTimeout(() => {
    if (noteModalRefs.starButtons && noteModalRefs.starButtons[0]) {
      try {
        noteModalRefs.starButtons[0].focus();
      } catch (_) {
        // ignore focus errors
      }
    }
  }, 60);
}

/**
 * Initialize the note modal (bind events, get references)
 */
export function initNoteModal() {
  const modalEl = document.getElementById('noteModal');
  if (!modalEl) return;

  noteModalRefs.modal = modalEl;
  noteModalRefs.textarea = modalEl.querySelector('#noteModalBody');
  noteModalRefs.sentimentButtons = Array.from(modalEl.querySelectorAll('#noteModalSentiment .feeling-pill'));
  noteModalRefs.starButtons = Array.from(modalEl.querySelectorAll('#noteModalStars i'));
  noteModalRefs.status = modalEl.querySelector('#noteModalStatus');
  noteModalRefs.saveButton = modalEl.querySelector('#noteModalSave');
  noteModalRefs.title = modalEl.querySelector('#noteModalLabel');
  noteModalRefs.charCount = modalEl.querySelector('#noteModalCharCount');
  noteModalRefs.ratingLabel = modalEl.querySelector('#noteModalRatingLabel');

  if (window.bootstrap && window.bootstrap.Modal) {
    noteModalInstance = window.bootstrap.Modal.getOrCreateInstance(modalEl);
  }

  noteModalRefs.starButtons.forEach((star) => {
    const val = parseInt(star.dataset.val, 10);
    star.addEventListener('mouseenter', () => paintNoteModalStars(val));
    star.addEventListener('mouseleave', () => paintNoteModalStars(noteModalState.rating));
    star.addEventListener('click', () => {
      noteModalState.rating = val;
      paintNoteModalStars(val);
    });
    star.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        noteModalState.rating = val;
        paintNoteModalStars(val);
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        e.preventDefault();
        const nextVal = Math.min(val + 1, 5);
        const next = noteModalRefs.starButtons[nextVal - 1];
        if (next) next.focus();
        paintNoteModalStars(nextVal);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        e.preventDefault();
        const prevVal = Math.max(val - 1, 1);
        const prev = noteModalRefs.starButtons[prevVal - 1];
        if (prev) prev.focus();
        paintNoteModalStars(prevVal);
      }
    });
  });

  noteModalRefs.sentimentButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const value = btn.dataset.sent || null;
      noteModalState.sentiment = noteModalState.sentiment === value ? null : value;
      paintNoteModalSentiment(noteModalState.sentiment);
    });
  });

  if (noteModalRefs.textarea && noteModalRefs.charCount) {
    noteModalRefs.textarea.addEventListener('input', () => {
      noteModalRefs.charCount.textContent = noteModalRefs.textarea.value.length;
    });
  }

  // Enter key to submit (from anywhere in modal except textarea with Shift)
  modalEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      // Allow Enter in textarea for newlines only with Shift
      if (e.target === noteModalRefs.textarea) {
        e.preventDefault();
      }
      // Trigger save if button is not disabled
      if (noteModalRefs.saveButton && !noteModalRefs.saveButton.disabled) {
        noteModalRefs.saveButton.click();
      }
    }
  });

  // Save button handler
  if (noteModalRefs.saveButton) {
    noteModalRefs.saveButton.addEventListener('click', async () => {
      if (!noteModalState.item || !noteModalState.learnerId) {
        if (noteModalRefs.status) {
          noteModalRefs.status.textContent = 'Missing item context';
        }
        return;
      }

      const raw = noteModalRefs.textarea ? noteModalRefs.textarea.value.trim() : '';
      if (noteModalRefs.status) {
        noteModalRefs.status.textContent = 'Saving…';
      }
      noteModalRefs.saveButton.disabled = true;

      try {
        const composed = composeFeedbackNote(raw, noteModalState.sentiment);
        await api('/v1/feedback', {
          method: 'POST',
          body: JSON.stringify({
            learner_id: noteModalState.learnerId,
            item_id: noteModalState.item.item_id || noteModalState.item.id,
            text: composed,
            rating: noteModalState.rating || null,
          }),
        });

        noteModalState.noteBody = raw;
        if (typeof noteModalState.onSave === 'function') {
          noteModalState.onSave({
            raw,
            sentiment: noteModalState.sentiment,
            composed,
            rating: noteModalState.rating,
          });
        }

        if (noteModalRefs.status) {
          noteModalRefs.status.textContent = 'Saved';
        }
        showToast('Review saved');

        setTimeout(() => {
          if (noteModalRefs.status) {
            noteModalRefs.status.textContent = '';
          }
        }, 1200);

        if (noteModalInstance) {
          noteModalInstance.hide();
        }
      } catch (err) {
        console.error(err);
        const msg = errorMessage(err, 'Failed to save review');
        if (noteModalRefs.status) {
          noteModalRefs.status.textContent = 'Failed';
        }
        showToast(msg);
      } finally {
        if (noteModalRefs.saveButton) {
          noteModalRefs.saveButton.disabled = false;
        }
      }
    });
  }

  paintNoteModalSentiment(noteModalState.sentiment);
  paintNoteModalStars(noteModalState.rating);

  // Reset state when modal is hidden
  modalEl.addEventListener('hidden.bs.modal', () => {
    // Call onClose callback before resetting state
    if (typeof noteModalState.onClose === 'function') {
      try {
        noteModalState.onClose();
      } catch (err) {
        console.error('Error in modal onClose callback:', err);
      }
    }
    noteModalState.item = null;
    noteModalState.learnerId = null;
    noteModalState.onSave = null;
    noteModalState.onClose = null;
    noteModalState.noteBody = '';
    noteModalState.sentiment = null;
    noteModalState.rating = 0;
    if (noteModalRefs.textarea) {
      noteModalRefs.textarea.value = '';
    }
    if (noteModalRefs.charCount) {
      noteModalRefs.charCount.textContent = '0';
    }
    if (noteModalRefs.status) {
      noteModalRefs.status.textContent = '';
    }
    paintNoteModalSentiment(null);
    paintNoteModalStars(0);

    // Restore focus to the element that was focused before modal opened
    if (previouslyFocusedElement && typeof previouslyFocusedElement.focus === 'function') {
      try {
        previouslyFocusedElement.focus();
      } catch (_) {
        // ignore focus errors if element is no longer in DOM
      }
    }
    previouslyFocusedElement = null;
  });

  // Focus trap - keep focus within modal when tabbing
  modalEl.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    const focusable = modalEl.querySelectorAll(
      'button:not([disabled]), textarea:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}

/**
 * Get current note modal state (for external access)
 * @returns {Object} Current modal state
 */
export function getNoteModalState() {
  return { ...noteModalState };
}

/**
 * Update note modal state externally
 * @param {Object} updates - State updates
 */
export function updateNoteModalState(updates) {
  Object.assign(noteModalState, updates);
}

export default {
  parseFeedbackNote,
  composeFeedbackNote,
  openNoteModal,
  initNoteModal,
  getNoteModalState,
  updateNoteModalState,
};
