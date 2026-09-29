import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useStore';
import { createAdThunk } from '../store/adsSlice';
import { useToast } from '../context/ToastContext';
import Spinner from '../components/Spinner';
import type { AdvertCreate } from '../types/api';

const CATEGORIES = [
  { value: 'other', label: 'Інше' },
  { value: 'electronics', label: 'Електроніка' },
  { value: 'clothing', label: 'Одяг' },
  { value: 'vehicles', label: 'Транспорт' },
  { value: 'realestate', label: 'Нерухомість' },
  { value: 'services', label: 'Послуги' },
  { value: 'furniture', label: 'Меблі' },
];

interface FormValues {
  name: string;
  description: string;
  price: string;
  category: string;
  tg_id: string;
}

interface FormErrors {
  name?: string;
  description?: string;
  price?: string;
  tg_id?: string;
}

const initialValues: FormValues = {
  name: '',
  description: '',
  price: '',
  category: 'other',
  tg_id: '',
};

const CreateAdPage = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const creating = useAppSelector((s) => s.ads.creating);

  const [values, setValues] = useState<FormValues>(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Partial<Record<keyof FormValues, boolean>>>({});

  // ── Validation ────────────────────────────────────────────────────────
  const validate = (vals: FormValues): FormErrors => {
    const errs: FormErrors = {};
    if (!vals.name.trim()) {
      errs.name = 'Назва є обов\'язковою';
    } else if (vals.name.trim().length < 3) {
      errs.name = 'Назва повинна містити щонайменше 3 символи';
    }
    if (!vals.description.trim()) {
      errs.description = 'Опис є обов\'язковим';
    } else if (vals.description.trim().length < 10) {
      errs.description = 'Опис повинен містити щонайменше 10 символів';
    }
    if (!vals.price) {
      errs.price = 'Ціна є обов\'язковою';
    } else if (isNaN(Number(vals.price)) || Number(vals.price) <= 0) {
      errs.price = 'Ціна повинна бути числом більше 0';
    }
    if (!vals.tg_id) {
      errs.tg_id = 'Telegram ID є обов\'язковим';
    } else if (!Number.isInteger(Number(vals.tg_id)) || Number(vals.tg_id) <= 0) {
      errs.tg_id = 'Telegram ID повинен бути цілим додатнім числом';
    }
    return errs;
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    const updated = { ...values, [name]: value };
    setValues(updated);
    if (touched[name as keyof FormValues]) {
      setErrors(validate(updated));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    setErrors(validate(values));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const allTouched = Object.fromEntries(
      Object.keys(values).map((k) => [k, true]),
    ) as Partial<Record<keyof FormValues, boolean>>;
    setTouched(allTouched);
    const errs = validate(values);
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    const payload: AdvertCreate = {
      name: values.name.trim(),
      description: values.description.trim(),
      price: Number(values.price),
      category: values.category,
      tg_id: Number(values.tg_id),
    };

    const result = await dispatch(createAdThunk(payload));
    if (createAdThunk.fulfilled.match(result)) {
      showToast(`✓ Оголошення "${payload.name}" успішно створено!`, 'success');
      navigate('/dashboard');
    } else {
      const errMsg = (result.payload as string) || 'Не вдалося створити оголошення';
      showToast(errMsg, 'error');
    }
  };

  const fieldError = (field: keyof FormErrors) =>
    touched[field] ? errors[field] : undefined;

  return (
    <div className="page create-page">
      <div className="page__header">
        <div>
          <h1 className="page__title">Нове оголошення</h1>
          <p className="page__subtitle">Заповніть форму для публікації оголошення</p>
        </div>
      </div>

      <div className="create-page__wrapper">
        <form
          className="create-form"
          onSubmit={handleSubmit}
          noValidate
          id="create-ad-form"
        >
          {/* Name */}
          <div className="form-group">
            <label className="form-label" htmlFor="ad-name">
              Назва <span className="form-required">*</span>
            </label>
            <input
              id="ad-name"
              name="name"
              className={`form-input ${fieldError('name') ? 'form-input--error' : ''}`}
              type="text"
              placeholder="Введіть назву оголошення..."
              value={values.name}
              onChange={handleChange}
              onBlur={handleBlur}
              disabled={creating}
              maxLength={200}
            />
            {fieldError('name') && (
              <p className="form-error" role="alert">{fieldError('name')}</p>
            )}
          </div>

          {/* Description */}
          <div className="form-group">
            <label className="form-label" htmlFor="ad-description">
              Опис <span className="form-required">*</span>
            </label>
            <textarea
              id="ad-description"
              name="description"
              className={`form-textarea ${fieldError('description') ? 'form-input--error' : ''}`}
              placeholder="Детальний опис товару або послуги..."
              value={values.description}
              onChange={handleChange}
              onBlur={handleBlur}
              disabled={creating}
              rows={4}
            />
            {fieldError('description') && (
              <p className="form-error" role="alert">{fieldError('description')}</p>
            )}
          </div>

          {/* Price + Category row */}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="ad-price">
                Ціна (₴) <span className="form-required">*</span>
              </label>
              <div className="form-input-wrapper">
                <span className="form-input-icon">₴</span>
                <input
                  id="ad-price"
                  name="price"
                  className={`form-input form-input--with-icon ${fieldError('price') ? 'form-input--error' : ''}`}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  placeholder="0"
                  value={values.price}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  disabled={creating}
                  min="1"
                />
              </div>
              {fieldError('price') && (
                <p className="form-error" role="alert">{fieldError('price')}</p>
              )}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="ad-category">
                Категорія
              </label>
              <select
                id="ad-category"
                name="category"
                className="form-select"
                value={values.category}
                onChange={handleChange}
                onBlur={handleBlur}
                disabled={creating}
              >
                {CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Telegram ID */}
          <div className="form-group">
            <label className="form-label" htmlFor="ad-tg-id">
              Telegram ID користувача <span className="form-required">*</span>
            </label>
            <div className="form-input-wrapper">
              <span className="form-input-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
              </span>
              <input
                id="ad-tg-id"
                name="tg_id"
                className={`form-input form-input--with-icon ${fieldError('tg_id') ? 'form-input--error' : ''}`}
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                placeholder="Наприклад: 123456789"
                value={values.tg_id}
                onChange={handleChange}
                onBlur={handleBlur}
                disabled={creating}
                min="1"
              />
            </div>
            {fieldError('tg_id') && (
              <p className="form-error" role="alert">{fieldError('tg_id')}</p>
            )}
          </div>

          {/* Actions */}
          <div className="form-actions">
            <button
              type="button"
              className="btn btn--ghost"
              onClick={() => navigate('/dashboard')}
              disabled={creating}
              id="cancel-create-btn"
            >
              Скасувати
            </button>
            <button
              type="submit"
              className="btn btn--primary"
              disabled={creating}
              id="submit-create-btn"
            >
              {creating ? (
                <>
                  <Spinner size={18} />
                  <span>Публікація...</span>
                </>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="12" y1="5" x2="12" y2="19"/>
                    <line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                  <span>Опублікувати</span>
                </>
              )}
            </button>
          </div>
        </form>

        {/* Preview panel */}
        <div className="create-page__preview">
          <h2 className="create-page__preview-title">Попередній перегляд</h2>
          <div className="ad-card ad-card--preview">
            <div className="ad-card__header">
              <span className="ad-card__category">
                {CATEGORIES.find((c) => c.value === values.category)?.label ?? 'Інше'}
              </span>
              <span className="badge badge--pending">На модерації</span>
            </div>
            <h3 className="ad-card__title">
              {values.name || <span className="placeholder-text">Назва оголошення</span>}
            </h3>
            <p className="ad-card__description">
              {values.description || <span className="placeholder-text">Опис оголошення...</span>}
            </p>
            <div className="ad-card__footer">
              <span className="ad-card__price">
                {values.price ? `${Number(values.price).toLocaleString('uk-UA')} ₴` : '— ₴'}
              </span>
              <span className="ad-card__user">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
                {values.tg_id || '—'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateAdPage;