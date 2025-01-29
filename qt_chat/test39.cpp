// 智能滚动控制
void MainWindow::conditionalScroll(bool forceCheck) {
    QScrollBar* scrollBar = ui->chatList->verticalScrollBar();
    
    bool shouldScroll = forceCheck ? 
        (scrollBar->value() == scrollBar->maximum()) :
        lastWasBottom;
        
    if (shouldScroll) {
        ui->chatList->scrollToBottom();
    }
    
    lastWasBottom = (scrollBar->value() == scrollBar->maximum());
}

// 更新消息示例
void MainWindow::updateMessage(int index) {
    QListWidgetItem* item = ui->chatList->item(index);
    if (!item) return;
    
    QLabel* label = qobject_cast<QLabel*>(ui->chatList->itemWidget(item));
    if (label) {
        // 保存当前滚动状态
        QScrollBar* scrollBar = ui->chatList->verticalScrollBar();
        int oldMax = scrollBar->maximum();
        int oldValue = scrollBar->value();
        bool wasAtBottom = (oldValue == oldMax);
        
        // 更新内容
        label->setText("Updated: " + QDateTime::currentDateTime().toString());
        label->adjustSize();
        item->setSizeHint(label->sizeHint());
        
        // 延迟滚动检查
        QTimer::singleShot(0, this, [this, wasAtBottom]() {
            conditionalScroll(wasAtBottom);
        });
    }
}