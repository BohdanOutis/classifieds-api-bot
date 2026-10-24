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

  // Утилітні класи для полів вводу
  const getInputClasses = (hasError?: string) =>
    `w-full px-4 py-3 bg-[var(--clr-surface-2)] border rounded-[var(--radius-sm)] text-[var(--clr-text)] text-sm outline-none transition-all duration-200 placeholder:text-[var(--clr-text-3)] disabled:opacity-50 ${
      hasError
        ? 'border-[var(--clr-rejected)]! focus:ring-3 focus:ring-red-500/10!'
        : 'border-[var(--clr-border)] focus:border-[var(--clr-accent)] focus:ring-3 focus:ring-[rgba(108,99,255,0.15)] focus:bg-[var(--clr-surface-3)]'
    }`;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[var(--clr-text)]">Нове оголошення</h1>
          <p className="text-sm text-[var(--clr-text-2)] mt-1">Заповніть форму для публікації оголошення</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-7 items-start">
        {/* Form */}
        <form
          className="bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-lg)] p-8 flex flex-col gap-6"
          onSubmit={handleSubmit}
          noValidate
          id="create-ad-form"
        >
          {/* Name */}
          <div className="flex flex-col gap-1.5">
            <label className="text-[0.8125rem] font-semibold text-[var(--clr-text-2)] tracking-wider uppercase" htmlFor="ad-name">
              Назва <span className="text-[var(--clr-rejected)] ml-0.5">*</span>
            </label>
            <input
              id="ad-name"
              name="name"
              className={getInputClasses(fieldError('name'))}
              type="text"
              placeholder="Введіть назву оголошення..."
              value={values.name}
              onChange={handleChange}
              onBlur={handleBlur}
              disabled={creating}
              maxLength={200}
            />
            {fieldError('name') && (
              <p className="flex items-center gap-1.5 text-[0.8125rem] text-[var(--clr-rejected)] animate-fade-in-up" role="alert">
                {fieldError('name')}
              </p>
            )}
          </div>

          {/* Description */}
          <div className="flex flex-col gap-1.5">
            <label className="text-[0.8125rem] font-semibold text-[var(--clr-text-2)] tracking-wider uppercase" htmlFor="ad-description">
              Опис <span className="text-[var(--clr-rejected)] ml-0.5">*</span>
            </label>
            <textarea
              id="ad-description"
              name="description"
              className={`${getInputClasses(fieldError('description'))} resize-y min-h-[100px]`}
              placeholder="Детальний опис товару або послуги..."
              value={values.description}
              onChange={handleChange}
              onBlur={handleBlur}
              disabled={creating}
              rows={4}
            />
            {fieldError('description') && (
              <p className="flex items-center gap-1.5 text-[0.8125rem] text-[var(--clr-rejected)] animate-fade-in-up" role="alert">
                {fieldError('description')}
              </p>
            )}
          </div>

          {/* Price + Category row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div className="flex flex-col gap-1.5">
              <label className="text-[0.8125rem] font-semibold text-[var(--clr-text-2)] tracking-wider uppercase" htmlFor="ad-price">
                Ціна (₴) <span className="text-[var(--clr-rejected)] ml-0.5">*</span>
              </label>
              <div className="relative flex items-center">
                <span className="absolute left-3.5 text-[var(--clr-text-3)] text-sm font-medium pointer-events-none">
                  ₴
                </span>
                <input
                  id="ad-price"
                  name="price"
                  className={`${getInputClasses(fieldError('price'))} pl-11`}
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
                <p className="flex items-center gap-1.5 text-[0.8125rem] text-[var(--clr-rejected)] animate-fade-in-up" role="alert">
                  {fieldError('price')}
                </p>
              )}
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-[0.8125rem] font-semibold text-[var(--clr-text-2)] tracking-wider uppercase" htmlFor="ad-category">
                Категорія
              </label>
              <select
                id="ad-category"
                name="category"
                className={`${getInputClasses()} appearance-none pr-10 cursor-pointer bg-[url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='16'%20height='16'%20viewBox='0 0 24 24'%20fill='none'%20stroke='%2394a3b8'%20stroke-width='2'%3E%3Cpolyline%20points='6 9 12 15 18 9'/%3E%3C/svg%3E")] bg-no-repeat bg-[right_12px_center]`}
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
          <div className="flex flex-col gap-1.5">
            <label className="text-[0.8125rem] font-semibold text-[var(--clr-text-2)] tracking-wider uppercase" htmlFor="ad-tg-id">
              Telegram ID користувача <span className="text-[var(--clr-rejected)] ml-0.5">*</span>
            </label>
            <div className="relative flex items-center">
              <span className="absolute left-3.5 text-[var(--clr-text-3)] pointer-events-none">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
              </span>
              <input
                id="ad-tg-id"
                name="tg_id"
                className={`${getInputClasses(fieldError('tg_id'))} pl-11`}
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
              <p className="flex items-center gap-1.5 text-[0.8125rem] text-[var(--clr-rejected)] animate-fade-in-up" role="alert">
                {fieldError('tg_id')}
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-3 justify-end pt-2">
            <button
              type="button"
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-[var(--radius-sm)] text-sm font-semibold bg-transparent border border-[var(--clr-border)] text-[var(--clr-text-2)] transition-all duration-200 cursor-pointer hover:enabled:text-[var(--clr-text)] hover:enabled:border-[var(--clr-border-hover)] hover:enabled:bg-[var(--clr-surface-3)] disabled:opacity-45 disabled:cursor-not-allowed"
              onClick={() => navigate('/dashboard')}
              disabled={creating}
              id="cancel-create-btn"
            >
              Скасувати
            </button>

            <button
              type="submit"
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-[var(--radius-sm)] text-sm font-semibold text-white bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 shadow-[0_4px_14px_var(--clr-accent-glow)] transition-all duration-200 cursor-pointer hover:enabled:bg-gradient-to-br hover:enabled:from-[var(--clr-accent-hover)] hover:enabled:to-purple-500 hover:enabled:shadow-[0_6px_20px_var(--clr-accent-glow)] hover:enabled:-translate-y-0.5 active:enabled:translate-y-0 disabled:opacity-45 disabled:cursor-not-allowed"
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
        <div className="sticky top-6 flex flex-col gap-4">
          <h2 className="text-[0.8125rem] font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">
            Попередній перегляд
          </h2>

          <div className="bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-lg)] p-5 flex flex-col gap-4">
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-[var(--clr-surface-2)] text-[var(--clr-text-2)]">
                {CATEGORIES.find((c) => c.value === values.category)?.label ?? 'Інше'}
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[0.7rem] font-bold tracking-wider uppercase bg-amber-500/15 text-amber-400 border border-amber-500/30">
                На модерації
              </span>
            </div>

            <h3 className="text-lg font-bold text-[var(--clr-text)] line-clamp-2">
              {values.name || <span className="text-[var(--clr-text-3)] italic">Назва оголошення</span>}
            </h3>

            <p className="text-sm text-[var(--clr-text-2)] line-clamp-3 whitespace-pre-wrap">
              {values.description || <span className="text-[var(--clr-text-3)] italic">Опис оголошення...</span>}
            </p>

            <div className="flex items-center justify-between pt-3 border-t border-[var(--clr-border)] text-sm">
              <span className="font-bold text-[var(--clr-accent-2)] text-base">
                {values.price ? `${Number(values.price).toLocaleString('uk-UA')} ₴` : '— ₴'}
              </span>
              <span className="flex items-center gap-1.5 text-xs text-[var(--clr-text-3)]">
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