def update_offer_status(self, offer_id: int, new_status: str, current_user_id: int) -> Offer:
    offer = self.get_offer(offer_id)

    # Логика: Принять предложение (accepted) может только создатель ЗАПРОСА
    if new_status == "accepted" and offer.request.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Только автор запроса может принять оффер")

    # Логика: Изменить на "отправлено" (shipped) может только баер
    if new_status == "shipped" and offer.buyer_id != current_user_id:
        raise HTTPException(status_code=403, detail="Только баер может отметить отправку")

    # Логика: Изменить на "доставлено" (delivered) может только покупатель
    if new_status == "delivered" and offer.request.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Только покупатель подтверждает получение")

    offer.status = new_status
    return self.repository.update(offer)
